"""R7: weighted finite-volume Maxwell weak-form vs exact ring Green action.

Do not confuse smooth manufactured probes with PH16 on-shell sources.
No source solver, Einstein solve, Lorentzian completion, or full exterior test.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import numpy as np
from scipy.sparse import diags

PH16_SHA = 'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
P10_SHA = '25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb'
P8_SHA = '406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed'
R3_SHA = '94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'
R6_SHA = '6b25e72395e69875ab64c1ca53c773b42ccf5a296b1487847cd313eb697df2be'
R6_VERIFY_SHA = '8dae2a70cf8ce00526640ab69c7fb3ec65a970fcb77e86f064a1da5a8a7c6129'


def sha(path):
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'MISSING'


def bump(x, radius):
    """C-infinity compactly supported manufactured scalar profile."""
    x = np.asarray(x, dtype=float)
    result = np.zeros_like(x)
    active = np.abs(x) < radius
    t = x[active]/radius
    result[active] = np.exp(1.-1./(1.-t*t))
    return result


def fit(K, L, mask=None):
    if mask is not None:
        K = K[np.ix_(mask, mask)]
        L = L[np.ix_(mask, mask)]
    s = float(np.sum(K*L)/np.sum(L*L))
    return {
        'scale': s,
        'relative_frobenius_mismatch': float(np.linalg.norm(K-s*L)/np.linalg.norm(K)),
    }


def energy_ratio(K, L, f):
    a = float(f@K@f)
    b = float(f@L@f)
    if a <= 0 or b <= 0:
        raise RuntimeError('NONPOSITIVE_QUADRATIC_ENERGY')
    return a/b


def mesh_audit(n, native=None):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource, Spec, JointAction, Settings,
    )
    # This constructs the ring quadrature operators, not any source solution.
    m = CoulombSource(Spec(nr=n, L=12.), self_order=8)
    j = JointAction(m, Settings(nr=n, L=12.))
    W = np.diag(m.w)
    Gx, Gy = m.wkernel, m.wmagkernel
    Kx, Ky = j.Kx, j.Ky

    # Matched finite-volume weak-form operators. Cylindrical m=1 needs 1/rho^2.
    L0 = W@m.L.toarray()
    L1 = W@(m.L.toarray()+np.diag(1./m.rho**2))
    inner = np.arange(m.cells).reshape(n, 2*n)[1:-1,1:-1].ravel()
    if (np.max(np.abs(L0-L0.T)) > 5e-12 or
        np.max(np.abs(L1-L1.T)) > 5e-12):
        raise RuntimeError('WEIGHTED_FINITE_VOLUME_NONRECIPROCITY')

    metrics = {}
    for label, K, G, L in [('X',Kx,Gx,L0), ('Y',Ky,Gy,L1)]:
        max_recip = float(np.max(np.abs(K-K.T)))
        inverse_resid = float(np.linalg.norm(K@G-W)/np.linalg.norm(W))
        if max_recip > 1e-10 or inverse_resid > 1e-10:
            raise RuntimeError('GREEN_INVERSE_IDENTITY_FAILED_'+label)
        metrics[label] = {
            'inverse_green_weight_identity_relative': inverse_resid,
            'reciprocity_inf': max_recip,
            'whole_fit': fit(K,L),
            'interior_fit': fit(K,L,inner),
            'green_dense_nonzeros': int(np.count_nonzero(K)),
            'weighted_fv_nonzeros': int(np.count_nonzero(L)),
        }

    probes = [
        ('compact_center', 7.,7.,0.),
        ('compact_shifted',6.,5.,2.),
        ('compact_wide',9.,8.,-1.),
    ]
    results = {'X':{}, 'Y':{}}
    negative = {}
    for name, radial_cutoff, axial_cutoff, offset in probes:
        base = bump(m.rho,radial_cutoff)*bump(m.z-offset,axial_cutoff)
        X = base
        Y = m.rho*base  # Smooth, regular A_phi at rho=0.
        for field,K,L in [('X',Kx,L0),('Y',Ky,L1)]:
            vec = X if field == 'X' else Y
            results[field][name] = energy_ratio(K,L,vec)
        # Negative control: omit compulsory m=1 azimuthal curvature.
        negative[name] = energy_ratio(Ky,L0,Y)
    output = {
      'nr': n, 'nz':2*n, 'h':float(m.h),
      'Green_vs_weighted_FV':metrics,
      'compact_smooth_energy_K_over_FV':results,
      'Y_wrong_missing_azimuthal_term_K_over_L0':negative,
      'probe_type':'PRESCRIBED_SMOOTH_OFF_SHELL_NOT_PH16_SOLUTIONS',
      'source_solve':'NOT_RUN',
      'actual_exterior':'NOT_DERIVED',
    }
    if native is not None:
        if n!=12:
            raise RuntimeError('NATIVE_PROFILE_ONLY_NR12')
        fields = {}
        for label,K,L,v in [('X',Kx,L0,native['A_X']),('Y',Ky,L1,native['A_Y'])]:
            if v.shape!=(m.cells,):
                raise RuntimeError('NATIVE_FIELD_SHAPE_DRIFT')
            Kv, Lv = K@v, L@v
            scale = float(np.dot(Kv,Lv)/np.dot(Lv,Lv))
            fields[label]={
              'K_over_FV_energy':energy_ratio(K,L,v),
              'K_minus_FV_gradient_relative':float(np.linalg.norm(Kv-Lv)/np.linalg.norm(Kv)),
              'on_field_best_scale':scale,
              'on_field_best_scaled_gradient_mismatch':float(np.linalg.norm(Kv-scale*Lv)/np.linalg.norm(Kv)),
            }
        output['native_R3_background'] = fields
    return output


def analyze(native):
    if any(native[k].shape!=(288,) for k in ('A_X','A_Y')):
        raise RuntimeError('R3_NATIVE_PROFILE_DRIFT')
    meshes = [mesh_audit(n, native if n==12 else None) for n in (8,12,16,20)]
    by_n = {str(x['nr']):x for x in meshes}
    improvements = {}
    for field in ('X','Y'):
        for probe in ('compact_center','compact_shifted','compact_wide'):
            deviation = [abs(m['compact_smooth_energy_K_over_FV'][field][probe]-1.) for m in meshes]
            # Only a finite four-mesh observation; not asymptotic certification.
            if not all(deviation[i+1]<deviation[i] for i in range(3)):
                raise RuntimeError('SMOOTH_PROBE_NONMONOTONIC_'+field+'_'+probe)
            improvements[field+'_'+probe]={
                'abs_energy_ratio_minus_one':deviation,
                'improves_on_all_four_meshes':True,
            }
    twelve = by_n['12']
    if (twelve['Green_vs_weighted_FV']['X']['interior_fit']['relative_frobenius_mismatch'] >= .10 or
        twelve['Green_vs_weighted_FV']['Y']['interior_fit']['relative_frobenius_mismatch'] >= .10):
        raise RuntimeError('FV_INTERIOR_COMPATIBILITY_FAILED')
    if any(by_n['20']['Y_wrong_missing_azimuthal_term_K_over_L0'][p] <=
           by_n['20']['compact_smooth_energy_K_over_FV']['Y'][p] for p in
           ('compact_center','compact_shifted','compact_wide')):
        raise RuntimeError('Y_AZIMUTHAL_NEGATIVE_CONTROL_FAILED')
    return {
      'mesh_sweep':meshes,
      'four_mesh_smooth_probe_trends':improvements,
      'scope':{
        'weighted_FV_operator':'W L_m0 for X; W (L_m0+diag(rho^-2)) for Y',
        'Green_operator':'inverse of original reciprocal ring Green with original self quadrature',
        'Schur_boundary_DtN':'NOT_CONSTRUCTED',
        'finite_mesh_energy_trend':'MEASURED_ON_OFF_SHELL_COMPACT_PROBES_ONLY',
        'native_actual_field_operator_compatibility':'NOT_CERTIFIED',
        'continuum_exterior':'NOT_CERTIFIED',
        'coupled_Lorentzian_health':'NOT_CERTIFIED',
        'Einstein_metric':'NOT_SOLVED',
        'Earth_down_whole_craft_up':'NOT_DERIVED',
        'complete_energy_lt10MJ':'NOT_CERTIFIED',
      },
    }
