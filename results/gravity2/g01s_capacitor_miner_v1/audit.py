"""Independent axisymmetric triangular-element audit of the two favorable
conditional stationary points. Independent mesh, basis, quadrature, fixed
charge field elimination and scalar iteration. Alter ground separation and
re-equilibrate all field degrees of freedom. Follows the source assumptions
of the named benchmark, including prescribed dark charges and pinned matter.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
from scipy.sparse import coo_matrix,diags,vstack
from scipy.sparse.linalg import splu
from scipy.interpolate import RectBivariateSpline
from scipy.optimize import root
from scipy.integrate import trapezoid
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
repo,out=map(Path,sys.argv[1:3])
cmp=json.loads((out/'comparison.json').read_text())
base=json.loads((out/'loaded.json').read_text())
if cmp['exp_loaded_sha256']!=sha(out/'loaded.json'): raise ValueError('parent drift')
C,G,U,R=299792458.,6.67430e-11,9e6,2.
K=C**4/(4*np.pi*G)
eta=base['eta']
a=base['inner_radius_m']
zc=np.sqrt(3.2**2-1)
def interpolation(tri,values,count):
    entries=np.broadcast_to(values,tri.shape)
    return coo_matrix((entries.ravel(),(np.repeat(np.arange(len(tri)),3),tri.ravel())),
                      shape=(len(tri),count)).tocsr()

class Triangular:
    def __init__(self,n):
        # Different from the finite-volume grid: polar-axis nodes included,
        # finite elements on triangles, outer boundary moved from 20 to 24 m.
        self.th=np.linspace(0,np.pi,n+1)
        self.r=np.unique(np.r_[np.linspace(0,a,n//4+1),np.linspace(a,R,n//4+1),
            np.linspace(R,3.6,n+1),np.linspace(3.6,6,n//2+1),np.geomspace(6,24,n//3+1)])
        rr,tt=np.meshgrid(self.r,self.th,indexing='ij')
        ids=np.arange(rr.size).reshape(rr.shape)
        lo,hi=ids[:-1,:-1].ravel(),ids[1:,1:].ravel()
        left,right=ids[1:,:-1].ravel(),ids[:-1,1:].ravel()
        tri=np.vstack([np.stack([lo,left,hi],1),np.stack([lo,hi,right],1)])
        rs,ts=rr.ravel()[tri],tt.ravel()[tri]
        area=((rs[:,1]-rs[:,0])*(ts[:,2]-ts[:,0])-(rs[:,2]-rs[:,0])*(ts[:,1]-ts[:,0]))
        def diff(x): return (np.roll(x,-1,axis=1)-np.roll(x,-2,axis=1))/area[:,None]
        self.m=n+1
        self.nodes=rr.size
        self.dim=rr.size-self.m
        D1=interpolation(tri,diff(ts),rr.size)[:,:self.dim].tocsr()
        D2=interpolation(tri,-diff(rs),rr.size)[:,:self.dim].tocsr()
        N=interpolation(tri,1/3,rr.size)[:,:self.dim].tocsr()
        rad=rs.mean(1); ang=ts.mean(1)
        W=np.pi*area*np.sin(ang)
        self.volume=W*rad**2
        self.wx=self.volume; self.wt=W
        stiff=D1.T@D1.multiply(self.wx[:,None])+D2.T@D2.multiply(W[:,None])
        self.scalar=(K/(eta*U)*(stiff+N.T@N.multiply(self.volume[:,None]))).tocsc()
        self.z=rad*np.cos(ang); rho=rad*np.sin(ang)
        cross=np.hypot(rho-1,self.z-zc)/.2
        smooth=np.clip(2*(1-cross),0,1)
        payload=self.volume*smooth**2*(3-2*smooth)
        # Independent discretization includes consistent surface mass elements.
        q=np.array([np.searchsorted(self.r,a),np.searchsorted(self.r,R)])
        surface_nodes=ids[q]
        si,sj=surface_nodes[:,:-1].ravel(),surface_nodes[:,1:].ravel()
        self.surface_mass=(.27*2*np.pi*np.array([a,R])[:,None]**2*(-np.diff(np.cos(self.th)))).ravel()
        surf=coo_matrix((np.full(si.size*2,.5),(np.tile(np.arange(len(si)),2),np.r_[si,sj])),
                         shape=(len(si),self.dim)).tocsr()
        self.B=vstack([N,surf],format='csr')
        self.payload=payload/payload.sum()
        source=(rad>a)&(rad<R)
        j0,j1=q*self.m
        active=slice(j0,j1+self.m)
        self.E1=D1[source,active].tocsr()
        self.E2=D2[source,active].tocsr()
        self.EN=N[source].tocsr()
        self.ew1=self.wx[source]; self.ew2=W[source]
        self.C0=4*np.pi/(1/a-1/R)
        self.seed=(1.1*np.exp(-.95*np.maximum(rr-2,0))/np.maximum(rr/2,1)).ravel()[:self.dim]
        self.tri_N=N

    def measure(self,k,H,y0=None):
        u=np.clip(.5-(self.z+H)/.15,0,1)
        mass=np.r_[self.payload+2000*self.volume*u*u*(3.-2*u),self.surface_mass]
        # Lump the material reaction term. A consistent mass matrix can
        # create alternating-sign tails inside the highly screened half-space.
        nodal_mass=self.B.T@mass
        coefficient=nodal_mass*k*C*C/U
        # In the reported weak metric regime the cubic-and-up change in
        # exp(k*y^2/2) is retained in the energy/gradient.
        prec=splu((self.scalar+diags(coefficient)).tocsc())
        cache={}
        def evaluate(y):
            ys=self.EN@y
            z=1+ys**2/2
            E=(self.E1.T@self.E1.multiply((self.ew1*z)[:,None])
              +self.E2.T@self.E2.multiply((self.ew2*z)[:,None])).tocsc()
            m=self.m
            block=E[m:-m,m:-m]
            voltage=np.r_[np.ones(m),splu(block).solve(-np.asarray(E[m:-m,:m].sum(1)).ravel()),np.zeros(m)]
            field=self.ew1*(self.E1@voltage)**2+self.ew2*(self.E2@voltage)**2
            cap=np.dot(z,field)
            drive=self.EN.T@(self.C0/cap**2*field*ys)
            v=y
            restgrad=coefficient*v*np.exp(.5*k*v*v)
            scalar=self.scalar@y
            energy=self.C0/cap+.5*np.dot(y,scalar)+C*C/U*np.dot(nodal_mass,np.expm1(.5*k*v*v))
            cache['energy']=energy
            return prec.solve(scalar+restgrad-drive)
        y=self.seed.copy() if y0 is None else y0.copy()
        # Relaxed field iteration followed by Jacobian-free Newton on its
        # Euler equation. No optimizer or charge law imported from producer.
        if y0 is None:
            for _ in range(42):
                residual=evaluate(y)
                if max(abs(residual))<.008: break
                y-=.4*residual
        sol=root(evaluate,y,method='krylov',options={'fatol':4e-9,'maxiter':25,'jac_options':{'rdiff':2e-6}})
        y=sol.x
        res=max(abs(evaluate(y))); energy=cache['energy']*U
        if res>2e-7 or energy>=U or min(y)<-1e-5: raise ValueError(('independent stationarity',res,energy,min(y),max(y)))
        sphere=np.r_[y,np.zeros(self.m)].reshape(-1,self.m)
        spline=RectBivariateSpline(self.r,self.th,sphere,kx=3,ky=3,s=0)
        s=np.linspace(0,.2,71)[:,None]
        t=np.arange(720)*2*np.pi/720
        x=(1+s*np.cos(t)).ravel(); zpos=(zc+s*np.sin(t)).ravel()
        r=np.hypot(x,zpos); theta=np.arctan2(x,zpos)
        dy=np.cos(theta)*spline.ev(r,theta,dx=1)-np.sin(theta)/r*spline.ev(r,theta,dy=1)
        minimum=min(-C*C*k*spline.ev(r,theta)*dy)
        ground=C*C*np.dot(self.tri_N.T@(2000*self.volume*6*u*(1-u)/.15),np.expm1(.5*k*y*y))
        return y,dict(energy_J=float(energy),minimum_up_m_s2=float(minimum),ground_reaction_N=float(ground),
                       Euler_residual=float(res))
checks=[]
for n in (78,138):
    mesh=Triangular(n)
    for k in (3e-14,3e-13):
        y,info=mesh.measure(k,3.)
        # Finite difference of re-equilibrated energies at fixed charge.
        h=.006 if n==78 else .003
        energies=[mesh.measure(k,3.+d,y)[1]['energy_J'] for d in (-h,h)]
        force=(energies[0]-energies[1])/(2*h)
        info.update(n_angle=n,k=k,shift_step_m=h,ground_force_by_work_N=force)
        checks.append(info)
        print('independent',n,k,info,flush=True)
assess=[]
for info in checks[-2:]:
    ref=next(r for r in cmp['loaded_field'] if r['n_theta']==240 and r['b_over_eta']==info['k'])
    diff_a=abs(info['minimum_up_m_s2']/ref['loaded_torus_min_up_m_s2']-1)
    diff_f=abs(info['ground_reaction_N']/ref['craft_portal_up_N']-1)
    work_error=abs(info['ground_force_by_work_N']/info['ground_reaction_N']-1)
    energy_error=abs(info['energy_J']/ref['total_active_static_J']-1)
    passed=max(diff_a,diff_f,work_error)<.02 and energy_error<.005
    assess.append(dict(k=info['k'],relative_acceleration_difference=diff_a,relative_force_difference=diff_f,
                 relative_energy_difference=energy_error,relative_force_work_difference=work_error,passes=bool(passed)))
status='PASS_SCOPED_TWO_DISCRETIZATIONS' if all(e['passes'] for e in assess) else 'HOLD_NUMERICAL_DISAGREEMENT'
report=dict(status=status,comparisons=assess,checks=checks,science_sha256=sha(out/'science.json'),
            comparison_sha256=sha(out/'comparison.json'),auditor_sha256=sha(Path(__file__)),
            source_realization='ASSUMED_DARK_ELECTRODE_CHARGES',full_regression='NOT_RUN',physical_survivors=0)
with (out/'independent.json').open('x') as f: json.dump(report,f,indent=2,sort_keys=True,allow_nan=False)
print(status,flush=True)
