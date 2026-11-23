"""Conditional hidden-photon benchmark. Minimize one static fixed-charge energy
over the scalar, with the Maxwell potential solved at every iterate. Conducting
concentric shells have equal opposite total charge and angular charge redistribution.
The hidden charge carriers are assumed. Electrode and payload masses move with
the craft; Earth is a fixed smoothed planar density. Gravity in the weight
comparison is prescribed. No mechanical support, carrier mass ledger, complete
metric dynamics, source material or microscopic hidden charges are derived.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import splu,spsolve
from scipy.interpolate import RegularGridInterpolator
from scipy.integrate import trapezoid
from scipy.optimize import root as solve_root

G,C,g=6.67430e-11,299792458.,9.80665
R,U0,mu=2.,9.e6,1.
X0=np.sqrt(3.2**2-1)
GAP=1.
GROUND_WIDTH=.15

def sha(f): return hashlib.sha256(f.read_bytes()).hexdigest()

def laplace(i,j,w,size):
    return coo_matrix((np.r_[w,w,-w,-w],(np.r_[i,j,i,j],np.r_[i,j,j,i])),
                      shape=(size,size)).tocsc()

def compact_torus(rho,z):
    s=np.hypot(rho-1,z-X0)/.2
    y=np.clip((1-s)*2,0,1)
    return y*y*(3-2*y)

class Section:
    def __init__(self,n,eta,inner,k,ground_density):
        self.k=k
        self.ls=C**4/(4*np.pi*G*eta*U0)
        self.inner=inner
        # Retain radial resolution around both foils, the payload and the
        # ground transition; Dirichlet far boundary is >15 vacuum ranges away.
        r=np.unique(np.r_[np.linspace(0,inner,n//5+1),np.linspace(inner,R,n//5+1),
                 np.linspace(R,4,n+1),np.linspace(4,7,n//2+1),np.geomspace(7,20,n//3+1)])
        theta=(np.arange(n)+.5)*np.pi/n
        edges=np.arange(n+1)*np.pi/n
        omega=2*np.pi*(np.cos(edges[:-1])-np.cos(edges[1:]))
        faces=np.r_[0,(r[1:]+r[:-1])/2,r[-1]]
        vol=np.diff(faces**3)[:,None]*omega/3
        rho,z=r[:,None]*np.sin(theta),r[:,None]*np.cos(theta)
        idx=np.arange(z.size).reshape(z.shape)
        ir,jr=idx[:-1].ravel(),idx[1:].ravel()
        it,jt=idx[:,:-1].ravel(),idx[:,1:].ravel()
        wr=((faces[1:-1]**2/np.diff(r))[:,None]*omega).ravel()
        wt=(2*np.pi*np.diff(faces)[:,None]*np.sin(edges[1:-1])/(np.pi/n)).ravel()
        L=laplace(np.r_[ir,it],np.r_[jr,jt],np.r_[wr,wt],z.size)
        self.free=idx[:-1].ravel()
        self.base=self.ls*(L+diags(mu**2*vol.ravel())).tocsc()[:-n,:-n].tocsc()
        i0,i1=map(int,np.searchsorted(r,[inner,R]))
        self.shell_mass=.27*4*np.pi*(inner**2+R**2)
        masses=np.zeros_like(z)
        for row in (i0,i1): masses[row]=.27*r[row]**2*omega
        raw=compact_torus(rho,z)*vol
        self.torus_mass_raw=float(raw.sum()*40/(23*.08*np.pi**2))
        masses+=raw/raw.sum()
        # Compact C1 transition. Negative density derivative produces an
        # equal and opposite ground force in the translation variation.
        u=np.clip((-(z+R+GAP)/GROUND_WIDTH+.5),0,1)
        masses+=ground_density*u**2*(3-2*u)*vol
        self.ground_slope=ground_density*(6*u*(1-u)/GROUND_WIDTH)*vol
        self.masses=masses.ravel()[:-n]
        self.metric_diag=self.masses*k*C**2/U0
        self.prec=splu(self.base+diags(self.metric_diag))
        self.r,self.theta,self.shape=r,theta,z.shape
        ids=idx[i0:i1+1]-i0*n
        er,es=ids[:-1].ravel(),ids[1:].ravel()
        et,eu=ids[1:-1,:-1].ravel(),ids[1:-1,1:].ravel()
        ewr=((r[i0:i1]*r[i0+1:i1+1]/np.diff(r[i0:i1+1]))[:,None]*omega).ravel()
        ewt=(2*np.pi*np.diff(faces)[i0+1:i1,None]*np.sin(edges[1:-1])/(np.pi/n)).ravel()
        self.ei,self.ej=np.r_[er,et],np.r_[es,eu]
        self.ew=np.r_[ewr,ewt]
        self.eshape=ids.shape
        self.eoff=i0*n
        self.c0=4*np.pi/(1/inner-1/R)

    def objective(self,y):
        n=len(self.theta); size=np.prod(self.eshape)
        i,j=self.ei,self.ej
        mid=.5*(y[self.eoff+i]+y[self.eoff+j])
        if np.max(abs(mid))>12: return np.inf,None,None
        ew=self.ew*np.exp(.5*mid*mid)
        A=laplace(i,j,ew,size)
        v=np.r_[np.ones(n),spsolve(A[n:-n,n:-n],-np.asarray(A[n:-n,:n].sum(1)).ravel()),np.zeros(n)]
        ev=ew*(v[i]-v[j])**2
        cap=ev.sum()
        em=self.c0/cap
        dg=-.5*em/cap*ev*mid
        em_grad=np.bincount(i+self.eoff,dg,minlength=len(y))+np.bincount(j+self.eoff,dg,minlength=len(y))
        sgrad=self.base@y
        s=.5*np.dot(y,sgrad)
        exponent=.5*self.k*y*y
        rest=np.dot(self.masses,np.expm1(exponent))*C**2/U0
        grad=sgrad+self.metric_diag*y*np.exp(exponent)+em_grad
        return em+s+rest,grad,[em,s,rest]

    def solve(self):
        r=self.r[:,None]
        z=np.ones(self.shape)*np.exp(-np.maximum(r-R,0))/np.maximum(r/R,1)
        y=z[:-1].ravel().copy()
        energy,grad,parts=self.objective(y)
        history=[]
        for it in range(260):
            q=grad.copy()
            alphas=[]
            for step,dg,inv in reversed(history):
                alpha=inv*np.dot(step,q)
                alphas.append(alpha)
                q-=alpha*dg
            vec=self.prec.solve(q)
            for (step,dg,inv),alpha in zip(history,reversed(alphas)):
                vec+=step*(alpha-inv*np.dot(dg,vec))
            res=np.max(abs(self.prec.solve(grad)))
            if res<2e-7: break
            if res<1e-4 and it%12==0:
                # Near a stationary point the energy difference loses digits
                # before the charge/eliminated gradient does. Finish on that
                # same gradient while retaining the original residual tolerance.
                def residual(candidate):
                    derivative=self.objective(candidate)[1]
                    return self.prec.solve(derivative)
                fixed=solve_root(residual,y,method="krylov",options={
                    "fatol":1e-7,"maxiter":12,"jac_options":{"rdiff":2e-6}})
                new_energy,new_grad,new_parts=self.objective(fixed.x)
                new_res=np.max(abs(self.prec.solve(new_grad)))
                if new_res<2e-7 and new_energy<=energy+1e-10:
                    y,energy,grad,parts,res=fixed.x,new_energy,new_grad,new_parts,new_res
                    break
            direction=-vec
            slope=np.dot(grad,direction)
            if slope>=0: raise ValueError("non-descent")
            length=1.
            for _ in range(28):
                new_y=y+length*direction
                val,new_g,new_parts=self.objective(new_y)
                if val<=energy+1e-4*length*slope+1e-15: break
                length*=.5
            else: raise ValueError("stationarity line search")
            step=new_y-y; dg=new_g-grad; curvature=np.dot(dg,step)
            if curvature>1e-17:
                history.append((step,dg,1/curvature)); history=history[-12:]
            y,energy,grad,parts=new_y,val,new_g,new_parts
        else: raise ValueError("stationarity iteration cap")
        y=np.r_[y,np.zeros(len(self.theta))].reshape(self.shape)
        if energy>=1 or np.min(y)<-1.e-5: raise ValueError("inactive or sign-changing branch")
        # A direct finite-difference derivative of assembled on-shell energy
        # checks the Maxwell fixed-charge elimination and scalar gradient.
        yy=y[:-1].ravel()
        direction=(1+.2*np.cos(self.theta)[None,:])*np.exp(-((self.r[:-1,None]-2)/1.4)**2)
        direction=direction.ravel()
        eps=2e-4
        eplus=self.objective(yy+eps*direction)[0]
        eminus=self.objective(yy-eps*direction)[0]
        slope_error=abs((eplus-eminus)/(2*eps)-np.dot(grad,direction))
        curvature=(eplus+eminus-2*energy)/eps**2
        # Derivatives evaluated on a finer target sampling independent of mesh.
        dr,dt=np.gradient(y,self.r,self.theta,edge_order=2)
        field=RegularGridInterpolator((self.r,self.theta),np.stack((y,dr,dt),axis=2))
        def physical(rho,z):
            dist=np.hypot(rho,z)
            angle=np.clip(np.arctan2(rho,z),self.theta[0],self.theta[-1])
            v,vr,vt=field(np.column_stack((dist,angle))).T
            return v,np.cos(angle)*vr-np.sin(angle)*vt/dist,np.sin(angle)*vr+np.cos(angle)*vt/dist
        angle=np.linspace(0,2*np.pi,512,endpoint=False)
        minor=np.linspace(0,.2,51)[:,None]
        rho=(1+minor*np.cos(angle)).ravel()
        z=(X0+minor*np.sin(angle)).ravel()
        vv,vz,_=physical(rho,z)
        acc=-C**2*self.k*vv*vz
        ground=C**2*np.sum(self.ground_slope*np.expm1(.5*self.k*y*y))
        # Independent field-stress integrals on two vacuum planes above ground.
        stress=[]
        for depth in (R+.4,R+.65):
            radial=np.linspace(0,np.sqrt((self.r[-1]-.05)**2-depth**2),4001)
            val,vz,vr=physical(radial,np.full_like(radial,-depth))
            stress.append(float(np.pi*self.ls*U0*trapezoid(radial*(vz*vz-vr*vr-(mu*val)**2),radial)))
        return dict(n_theta=len(self.theta),n_radial=len(self.r),steps=it,preconditioned_residual=float(res),
              torus_mass_before_discrete_normalization_kg=self.torus_mass_raw,torus_mass_kg=1.,
              scalar_curvature_check=float(curvature),gradient_FD_error=float(slope_error),
              electric_scalar_rest_increment_J=(np.array(parts)*U0).tolist(),total_active_static_J=float(energy*U0),
              loaded_torus_min_up_m_s2=float(min(acc)),loaded_torus_max_up_m_s2=float(max(acc)),
              craft_portal_up_N=float(ground),ground_up_N=float(-ground),vacuum_plane_stress_N=stress,
              mass_foil_and_torus_kg=self.shell_mass+1.,maximum_log_mass_shift=float(.5*self.k*np.max(y*y)),
              maximum_log_gauge_factor=float(.5*np.max(y*y)),maximum_log_gauge_in_torus=float(.5*np.max(vv*vv)))

def main(out):
    doc=json.loads((out/"science.json").read_bytes())
    check=json.loads((out/"verification.json").read_bytes())
    if check["science_sha256"]!=sha(out/"science.json"): raise ValueError("science drift")
    radii=np.array(doc["inner_radius_m"]); ai=np.argmin(abs(radii-1.5))
    finite=np.array(doc["range_m"][1:]); mi=1+np.argmin(abs(np.log(finite/1.)))
    a=float(radii[ai])
    # Compute the exact 1 m-range threshold for this seed via radial Ritz.
    # Reuse only atlas threshold function for choosing a nominal drive;
    # the 2D equilibrium is variational and does not use a radial field map.
    import importlib.util
    spec=importlib.util.spec_from_file_location("atlas",out/"produce.py")
    atlas=importlib.util.module_from_spec(spec); spec.loader.exec_module(atlas)
    eta=3.*atlas.threshold(1.,a,256)*1e7/U0
    runs=[]
    # The final case is a vacuum-ground null, keeping the loaded torus and walls.
    for coupling,density,meshes in [(3e-15,2000.,(64,112)),(3e-14,2000.,(64,112,176)),(3e-14,0.,(112,))]:
        for n in meshes:
            sec=Section(n,eta,a,coupling,density)
            row=sec.solve()
            row.update(b_over_eta=coupling,ground_kg_m3=density)
            print(n,coupling,density,"a_min",row["loaded_torus_min_up_m_s2"],"force",row["craft_portal_up_N"],
                  "plane",row["vacuum_plane_stress_N"],flush=True)
            runs.append(row)
    record=dict(status="CONDITIONAL_FIXED_GEOMETRY_HIDDEN_CHARGE_BENCHMARK",rows=runs,action=__doc__,
             eta=eta,uncharged_scalar_phi=0.,unscalarized_charged_energy_J=U0,range_m=1.,inner_radius_m=a,
             ground_interface_width_m=GROUND_WIDTH,ground_nominal_clearance_m=GAP,surface_density_kg_m2=.27,
             reference="relative to uncharged, phi=0. Static field and conformal rest shift included; no battery, supports, switching or shell mechanical energy.",
             validation="separate ground-density translation and vacuum planes; positive curvature in one test direction is not full modal stability",
             science_sha256=sha(out/"science.json"),source_sha256=sha(Path(__file__)),physical_survivors=0,
             full_regression="NOT_RUN")
    return record

if __name__=="__main__":
    folder=Path(sys.argv[2])
    with (folder/"loaded.json").open("x") as f:
        json.dump(main(folder),f,sort_keys=True,indent=2,allow_nan=False)
