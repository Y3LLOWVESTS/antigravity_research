"""G01-R postcheck: empirical transfer and all-range positive-energy bound.

For freely diagonalized, unscreened canonical scalars of strengths b_i, set
a=-c^2 sum b_i grad(phi_i). Cauchy-Schwarz pointwise and integration over
the full target give sum(U_i)*sum(b_i^2)>=g^2*V/(8*pi*G). This bounds the
driven field energy using a zero off-state (or just the quadratic norm of the
on-minus-off field). Positive scalar exchange between ordinary masses has
Yukawa/Newton coefficient b_i^2 in the same normalization. For any pair of
nonoverlapping spheres on the centerline, each projected Newton kernel is
positive, hence its weighted Yukawa ratio is >=(1+x)*exp(-x), with x the
maximum pair-element distance divided by the shortest range. No assumption on
EM source shape. Couplings/charges must remain universal and unscreened.
These are model predictions for the two masses, not a refit of the apparatus.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import numpy as np

def main():
    run=Path(sys.argv[1]).resolve()
    science=json.loads((run/"science.json").read_bytes())
    verify=json.loads((run/"verification.json").read_bytes())
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    if verify['science_sha256']!=sha(run/'science.json') or verify['status']!='PASS_SCOPED':
        raise ValueError('independent numerical verdict required')
    G=6.67430e-11
    floor=9.80665**2*2*math.pi**2*.2**2/(8*math.pi*G)
    if abs(floor/verify['target_only_alpha2_energy_J']-1)>1e-13:
        raise ValueError('finite-target units')
    band=(.2,2.)
    cap=.012   # Goodkind et al.: |Yukawa coefficient| < 0.012 G (95%).
    rows=[r for r in science['levels'][-1]['rows'] if r['mu_per_m'] and band[0]<=1/r['mu_per_m']<=band[1]]
    rb,ab=verify['best_relaxed_index'],verify['best_axial_index']
    bests=[]
    for index,energy in ((rb,verify['minimum_relaxed_alpha2_energy_J']),(ab,verify['minimum_axial_alpha2_energy_J'])):
        r=science['levels'][-1]['rows'][index]
        if r not in rows: raise ValueError('best outside published band')
        bests.append(dict(range_m=1/r['mu_per_m'],required_strength_strict_min=energy/1e7,
                          scalar_energy_at_lab_limit_J=energy/cap,
                          strength_factor_over_lab_cap=(energy/1e7)/cap))
    # Independent two-sphere density integration using positive projected
    # pair forces. Split uniform balls into Gaussian axial slices, rings and
    # relative azimuth, integrate both Newton and Yukawa via the same weights.
    x,w=np.polynomial.legendre.leggauss(12)
    z,r=np.meshgrid(x,(x+1)/2,indexing="ij")
    radius=np.sqrt(1-z*z)*np.sqrt(r)*.001
    z=(.001*z).ravel()
    radius=radius.ravel()
    volumes=(np.outer(w,w)*(1-(z/.001).reshape(12,12)**2)).ravel()
    azimuth=np.arange(64)*2*np.pi/64
    checks=[]
    for d in (.0025,.0058):
        dz=d+z[None,:]-z[:,None]
        den=num=0.
        for angle in azimuth:
            s=np.sqrt(dz**2+radius[:,None]**2+radius[None,:]**2-2*np.cos(angle)*np.outer(radius,radius))
            weight=np.outer(volumes,volumes)*dz/s**3
            den+=weight.sum()
            num+=(weight*(1+s/.03)*np.exp(-s/.03)).sum()
        # Uniform sphere Yukawa form factor, stable small-x series.
        x0=.001/.03
        form=1+x0**2/10+x0**4/280+x0**6/15120
        theory=(1+d/.03)*math.exp(-d/.03)*form**2
        if abs(num/den-theory)>1e-7: raise ValueError('two-sphere quadrature drift')
        checks.append(dict(d_m=d,force_ratio_per_unit_strength=num/den,analytic=theory))
    x_max=(.0058+2*.001)/.03
    y_min=(1+x_max)*math.exp(-x_max)
    result=dict(derivation=__doc__,inputs=dict(Westphal_DOI="10.1038/s41586-021-03250-7",
          sphere_radius_m=.001,center_range_m=[.0025,.0058],Goodkind_DOI="10.1103/PhysRevD.47.1290",
          published_Yukawa_strength_max=cap,published_range_m=band,confidence=.95),
          verdict="NO_ENERGY_LAB_OVERLAP_IN_DIRECT_PUBLISHED_BAND",
          sampled_rows_in_band=len(rows),continuous_band_target_only_energy_floor_J=floor/cap,
          near_optima=bests,model_minimum_sum_scalar_strength_at_10MJ=floor/1e7,
          all_lambda_ge_3cm_pair_kernel_minimum=y_min,predicted_extra_force_over_Newton_strict_min=y_min*floor/1e7,
          two_sphere_checks=checks,raw_laboratory_fit=False,conditional_on_ordinary_scalar_charges=True,
          verification_sha256=sha(run/'verification.json'),science_sha256=sha(run/'science.json'),
          postcheck_sha256=sha(Path(__file__)))
    raw=(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    dest=run.with_name(run.name+'_constraints.json')
    if not dest.exists():
        with tempfile.NamedTemporaryFile(dir=dest.parent) as tmp:
            tmp.write(raw); tmp.flush()
            os.link(tmp.name,dest)
    if dest.read_bytes()!=raw: raise ValueError('postcheck output drift')
    print('CONSTRAINTS_SHA256',sha(dest),dest)
    print('min additional sphere-pair force / Newton',result['predicted_extra_force_over_Newton_strict_min'])
    print('lab band',result['near_optima'])

if __name__=='__main__': main()
