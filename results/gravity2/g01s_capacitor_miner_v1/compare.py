"""G01-S constitutive sensitivity and independent controls (version 1).
Test Z=1+eta*phi^2/2 exactly, sharing only its onset Hessian with the
exponential model. Both are mathematical laws with hypothetical parameters.
Independently compare the unloaded sphere with radial nonlinear shooting/
collocation, integrate two distinct vacuum stress planes, and refine the loaded and vacuum
calculations. No physical hidden charge carriers are supplied.
"""
from pathlib import Path
import hashlib
import json
import sys
import importlib.util
import numpy as np
from scipy.integrate import solve_bvp
from scipy.sparse.linalg import splu
from scipy.sparse import diags
from scipy.optimize import minimize_scalar

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
root,out=map(Path,sys.argv[1:3])
spec=importlib.util.spec_from_file_location("exp_provider",out/"loaded.py")
common=importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)
C,G,g=common.C,common.G,common.g
doc=json.loads((out/"loaded.json").read_bytes())
atlas=json.loads((out/"science.json").read_bytes())
if doc['source_sha256']!=sha(out/'loaded.py') or doc['science_sha256']!=sha(out/'science.json'):
    raise ValueError('parent mismatch')
a,R,eta,U=doc['inner_radius_m'],2.,doc['eta'],common.U0
delta=1/a-1/R

class PolynomialSection(common.Section):
    def objective(self,y):
        n=len(self.theta)
        size=np.prod(self.eshape)
        i,j=self.ei,self.ej
        mid=.5*(y[self.eoff+i]+y[self.eoff+j])
        weights=self.ew*(1+.5*mid*mid)
        A=common.laplace(i,j,weights,size)
        boundary=-np.asarray(A[n:-n,:n].sum(1)).ravel()
        v=np.r_[np.ones(n),splu(A[n:-n,n:-n]).solve(boundary),np.zeros(n)]
        diff=v[i]-v[j]
        cap=np.dot(weights,diff*diff)
        em=self.c0/cap
        correction=-.5*self.c0/cap**2*self.ew*mid*diff**2
        egrad=np.bincount(self.eoff+i,correction,minlength=len(y))+np.bincount(self.eoff+j,correction,minlength=len(y))
        basegrad=self.base@y
        scalar=.5*np.dot(y,basegrad)
        z=.5*self.k*y*y
        rest=np.dot(self.masses,np.expm1(z))*C**2/U
        grad=basegrad+egrad+self.metric_diag*np.exp(z)*y
        return em+scalar+rest,grad,[em,scalar,rest]

def radial(k):
    # Independent radial elimination of Q. Variable r is in meters; phi
    # is regular in the empty inner ball and decays outside the outer foil.
    source=eta*U*G/(C**4*delta)
    b=eta*k
    jump=4*np.pi*G*b*.27/C**2
    def ode(r,Y):
        y,dy=Y
        return np.vstack([dy,(1-source/(r**4*(1+.5*y*y)**2))*y-2*dy/r])
    def bc(L,H):
        return [L[1]-(1/np.tanh(a)-1/a+jump*np.exp(.5*k*L[0]**2))*L[0],
                H[1]+(1+1/R+jump*np.exp(.5*k*H[0]**2))*H[0]]
    r=np.linspace(a,R,130)
    sol=solve_bvp(ode,bc,r,np.array([np.ones_like(r)*2,np.zeros_like(r)]),tol=2e-9,max_nodes=3000)
    if sol.status or sol.y[0,-1]<1e-6: raise ValueError('radial control inactive')
    surface=sol.y[0,-1]
    def accel(t):
        x,z=1+.2*np.cos(t),common.X0+.2*np.sin(t)
        r=np.hypot(x,z)
        y=surface*R/r*np.exp(-(r-R))
        return k*C**2*y*y*(1+1/r)*z/r
    return minimize_scalar(accel,bounds=(-np.pi/2,np.pi/2),method='bounded').fun

def run(k,density,meshes,empty=False):
    rows=[]
    for n in meshes:
        section=PolynomialSection(n,eta,a,k,density)
        if empty:
            rr,tt=section.r[:,None],section.theta
            rho,z=rr*np.sin(tt),rr*np.cos(tt)
            f=np.r_[0,(section.r[1:]+section.r[:-1])/2,section.r[-1]]
            volume=np.diff(f**3)[:,None]*2*np.pi*(-np.diff(np.cos(np.linspace(0,np.pi,n+1))))/3
            raw=common.compact_torus(rho,z)*volume
            section.masses-=raw.ravel()[:-n]/raw.sum()
            section.metric_diag=section.masses*k*C**2/U
            section.prec=splu(section.base+diags(section.metric_diag))
        try:
            result=section.solve()
        except ValueError as e:
            result=dict(n_theta=n,status="HOLD_NUMERICAL_OR_INACTIVE",reason=str(e))
        else:
            for key in ("maximum_log_gauge_factor","maximum_log_gauge_in_torus"):
                result[key]=np.log1p(result[key])
            result.update(status="SOLVED",torus_mass_kg=0. if empty else 1.)
        result.update(b_over_eta=k,ground_kg_m3=density,empty_torus=empty)
        print(n,k,density,'empty',empty,result['status'],result.get('loaded_torus_min_up_m_s2'),
              result.get('craft_portal_up_N'),result.get('vacuum_plane_stress_N'),flush=True)
        rows.append(result)
    return rows

field=[]
for k in (3e-15,3e-14,3e-13,3e-12):
    field.extend(run(k,2000.,(64,112)))
# Refine independent of whether 1 g is met. Follow the best minimum acceleration
# per tested k among computed medium-grid rows; also refine the fixed 3e-14 lane.
candidates=[r for r in field if r['status']=='SOLVED' and r['n_theta']==112]
if candidates:
    winner=max(candidates,key=lambda r:r['loaded_torus_min_up_m_s2'])['b_over_eta']
    for k in sorted({winner,3e-14}):
        field.extend(run(k,2000.,(176,240)))
else: winner=None
control=run(3e-14,0.,(64,112,176),empty=True)
rad=radial(3e-14)
controls=[abs(r['loaded_torus_min_up_m_s2']/rad-1) for r in control if r['status']=='SOLVED']
mix=[]
# Charge direction n=(sqrt(1-s),sqrt(s)); Maxwell metric diag(1,Z).
# At vacuum, d(log alpha_EM)/d(eta phi^2/2)=-s. Identical projection
# s for the fixed ordinary capacitor's charged field energy. An independent
# dark drive can have different source projection. Verify both derivatives.
for frac in (0.,1e-4,.01,.25,.5,1.):
    n=np.sqrt([1-frac,frac])
    def response(t): return n@np.linalg.solve(np.diag([1.,1+t]),n)
    h=1e-5
    slope=(response(h)-response(-h))/(2*h)
    if abs(slope+frac)>2e-10: raise ValueError("mixed photon derivative")
    mix.append([frac,slope])
summary=[]
for k in sorted({r['b_over_eta'] for r in field}):
    group=sorted([r for r in field if r['b_over_eta']==k and r['status']=='SOLVED'],key=lambda r:r['n_theta'])
    if len(group)<2: continue
    p,r=group[-2:]
    accel=r['loaded_torus_min_up_m_s2']; force=r['craft_portal_up_N']
    da=abs(p['loaded_torus_min_up_m_s2']/accel-1) if accel else None
    df=abs(p['craft_portal_up_N']/force-1) if force else None
    stress=max(abs(np.asarray(r['vacuum_plane_stress_N'])/force-1)) if force else None
    summary.append(dict(k=k,finest_n=r['n_theta'],min_up=accel,ground_up_on_craft_N=force,
          carried_weight_N=r['mass_foil_and_torus_kg']*g,accel_refinement_change=da,force_refinement_change=df,
          stress_relative_difference=stress,
          conditional_numerical_thresholds_met=bool(r['n_theta']>=176 and accel>=g and force>=r['mass_foil_and_torus_kg']*g
          and da is not None and da<.02 and df<.02 and stress<.03 and len(controls)==3 and controls[-1]<.01)))
result=dict(law="Z=1+eta phi^2/2",source_sha256=sha(Path(__file__)),exp_loaded_sha256=sha(out/'loaded.json'),
        vacuum_radial_min_up=rad,radial_control_relative_errors=controls,zero_ground_empty_torus=control,
        loaded_field=field,summaries=summary,selected_k=winner,mixing_checks=mix,
        ordinary_charge_projection_ratio_necessary_max=1/atlas['minimum_interval_mismatch_factor'],
        projection_domain="massless canonical photon mixing, fixed ordinary charge, leading material sensitivities",
        physical_survivors=0,full_regression='NOT_RUN')
with (out/'comparison.json').open('x') as f: json.dump(result,f,sort_keys=True,indent=2,allow_nan=False)
