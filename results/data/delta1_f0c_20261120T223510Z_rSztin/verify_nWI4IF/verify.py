"""Independent reconstruction of F0C from the flipped-mesh nodal potentials."""
import hashlib, json, math, sys, time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

dst=Path(__file__).resolve().parent
run=dst.parent
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

checks={}
def check(key,ok):
    checks[key]=bool(ok)
    if not ok:
        raise ValueError(key)

start=time.perf_counter()
v=dict(utc=datetime.now(timezone.utc).isoformat(),verifier=sha(Path(__file__)),
       checks=checks,full_regression="PENDING",next="NO_AUTOMATIC_PROMOTION")
try:
    p=run/"science.json"
    j=json.loads(p.read_bytes())
    v["science_sha256"]=sha(p)
    check("science sidecar", (run/"science.json.sha256").read_text().split()==[sha(p),"science.json"])
    check("completed producer",j["status"]=="LOADED_AXIAL_TRIAL_COMPLETE_PHYSICAL_MODE_UNDERDETERMINED" and sha(run/"f0c.py")==j["producer"])
    parents=j["parents"]
    check("pinned F0B",any(k.endswith("Gmr1NE/science.json") and h=="fd21173471942c8e21b2659d25ac8a8b3790ede8f0dce45717d4e38f7206963c" for k,h in parents.items()))
    check("parent bytes",all(sha(Path(k))==h for k,h in parents.items()))
    base=next(Path(k) for k in parents if k.endswith("b0_inverse_loading_summary.json"))
    minimum=next(g["fully_loaded_min_a_m_s2"] for g in json.loads(base.read_bytes())["grids"] if g["h_m"]==0.05)
    check("historical loaded failure",abs(minimum+129.67185782242464)<1e-10)
    # Eliminate both field variables directly in the isolated spherical action.
    E,B=np.linalg.solve([[3,.25],[.25,-1.5]],[-1,0])
    check("isolated curvature",abs(-.35-E-j["isolated_curvature"])<1e-13)
    check("unloaded bound",abs(j["loaded_uniform_curvature_upper"]+1/60)<1e-14)
    # d(j1)/dx=0 written using ordinary trigonometric functions.
    root=brentq(lambda x:(x*x-2)*math.sin(x)+2*x*math.cos(x),2,2.2)
    check("silent threshold",abs(.35/root**2-j["silent_k_over_R2_threshold"])<1e-13)
    rows=j["rows"]
    check("mesh experiment",[(t["case"],t["h"],t["L"],t["flip"]) for t in rows]==[
        ("off",.075,6,False),("vacuum",.075,6,False),("loaded",.075,6,False),
        ("loaded",.05,6,False),("loaded",.05,7.5,False),("loaded",.05,7.5,True)])
    check("portal off",rows[0]["minimum"]==rows[0]["maximum"]==0)
    check("unloaded dipole",rows[1]["minimum"]>0 and abs(rows[1]["curvature"]-(-.35-E))<.03)
    check("mass quadrature",all(abs(t["mass_kg"]-1)<.02 for t in rows))
    row=rows[-1]
    npz=run/"potentials.npz"
    check("saved fields",sha(npz)==row["potentials_sha256"])
    with np.load(npz,allow_pickle=False) as f:
        phi,psi=f["phi"],f["psi"]
    h,L=row["h"],row["L"]
    n=round(L/h)
    check("shape",phi.shape==psi.shape==(2*n+1,n+1))
    check("boundary",all(np.max(abs(u[[0,-1],:]))==0 and np.max(abs(u[:,-1]))==0 for u in (phi,psi)) and np.max(abs(psi[:,0]))==0)
    rz,zz=np.meshgrid(np.arange(n)*h,(np.arange(2*n)-n)*h)
    z0=math.sqrt(3.2**2-1)
    st=(np.s_[:-1,:-1],np.s_[:-1,1:],np.s_[1:,:-1],np.s_[1:,1:])
    gauss,amp,drive=(np.zeros_like(phi) for _ in range(3))
    metric=np.zeros_like(rz)
    mass=0.
    sums=np.zeros(5)
    for high in (False,True):
        u,w,x,y=[phi[t] for t in st]
        f,g,k,m=[psi[t] for t in st]
        off=(2 if high else 1)/3
        r,z=rz+off*h,zz+off*h
        if high:
            er,ez=(x-y)/h,(w-y)/h
            br,bz=(g-m)/(h*r),(m-k)/(h*r)
            corners=[(1,0,-1),(3,1,1),(2,-1,0)]
        else:
            er,ez=(u-w)/h,(u-x)/h
            br,bz=(f-k)/(h*r),(g-f)/(h*r)
            corners=[(0,-1,-1),(1,1,0),(2,0,1)]
        s=np.hypot(r-1,z-z0)/.2
        t=np.clip(2*(1-s),0,1)
        profile=t*t*(3-2*t)
        density=profile/(2*math.pi**2*.2**2*(23/40))
        # Archived, independently pinned peak for its 1-kg / 1-keV normalization.
        ball=np.hypot(r,z)<2
        theta=.25*ball+18987.283771593688*profile
        wt=math.pi*r*h*h
        Wb=wt*ball
        sums+=np.array([Wb.sum(),(Wb*z).sum(),(Wb*ez).sum(),(Wb*z*ez).sum(),(Wb*r*er).sum()])
        mass+=float(np.sum(wt*density))
        metric-=.125*(er*br+ez*bz)
        for slot,dr,dz in corners:
            ij=st[slot]
            gauss[ij]-=wt*((er+theta*br)*dr+(ez+theta*bz+ball)*dz)/h
            amp[ij]+=wt*((bz-theta*ez)*dr-(br-theta*er)*dz)/(h*r)
            drive[ij]+=wt*ball*dz/h
    norm=np.linalg.norm(drive[1:-1,:-1])
    weak=max(np.linalg.norm(gauss[1:-1,:-1]),np.linalg.norm(amp[1:-1,1:-1]))/norm
    v["independent_weak_residual"]=float(weak)
    check("corrected Gauss and Ampere",weak<1e-7)
    vol,mz,se,ze,re=sums
    check("material variation",abs((ze-mz*se/vol-.5*re)/(2*vol)-row["source_quadrupole_work"])<1e-12)
    check("full 1 kg trace",abs(mass-row["mass_kg"])<1e-11 and abs(row["peak_beta"]-18987.283771593688)<1e-8)
    R,Z=rz+h/2,zz+h/2
    mask=np.hypot(R-1,Z-z0)<.2
    accel=-(metric[2:]-metric[:-2])/(2*h)
    idx=np.unravel_index(np.argmin(np.where(mask[1:-1],accel,np.inf)),accel.shape)
    i,k=idx
    check("worst point",np.allclose([R[i+1,k],Z[i+1,k]],row["worst_r_z_m"],atol=1e-10,rtol=0))
    check("signed minimum",np.isclose(accel[idx],row["minimum"],rtol=1e-7,atol=1e-13))
    # A line integral of -d(log Omega)/dz on a fixed material chord.
    col=np.array([np.interp(1.,R[0],slice_) for slice_ in metric])
    lo,hi=np.interp([z0-.1,z0+.1],Z[:,0],col)
    check("chord work",np.isclose((lo-hi)/.2,row["chord_mean"],rtol=1e-7,atol=1e-13))
    v["minimum_changes_mesh_box_diagonal"]=[abs(rows[t+1]["minimum"]-rows[t]["minimum"]) for t in (2,3,4)]
    # The constrained field Hamiltonian is (|D-P-theta*B|^2+|B|^2)/2.
    # B=0 and the ordinary sphere displacement are admissible for any theta.
    # The field minimum is therefore bounded above by the vacuum cost.
    check("variational trial bound sign",(-.35+1/3)<0)
    # For the tangential solenoidal perturbation the field source is zero.
    # At fixed a, positive gradient stiffnesses on either side of kcrit give
    # opposite curvatures for exactly the same torus and trace coefficient.
    kc=j["silent_k_over_R2_threshold"]
    check("silent mode stiffness ambiguity",-.35+.5*kc*root**2<0<-.35+2*kc*root**2)
    check("uncertainty ledger",np.allclose(v["minimum_changes_mesh_box_diagonal"],j["trial_diagnostics"]["minimum_changes_mesh_box_diagonal"]) and j["trial_diagnostics"]["continuum_outcome"]=="NUMERICAL_INCONCLUSIVE")
    check("physical stop",j["physical_minimum"] is None and j["energy"]=="ENERGY_UNDETERMINED" and j["earth_craft"]=="NOT_DERIVED")
    v["status"]="PASS_SCOPED_TRIAL_AND_MODE_OBSTRUCTION"
except Exception as exc:
    v.update(status="HOLD",error=repr(exc))
v["wall_s"]=time.perf_counter()-start
raw=(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
with (dst/"verification.json").open("xb") as f:
    f.write(raw)
key=hashlib.sha256(raw).hexdigest()
with (dst/"verification.json.sha256").open("x") as f:
    f.write(f"{key}  verification.json\n")
print(v["status"],sum(checks.values()),"/",len(checks),key,v.get("error",""))
print("VERIFICATION_JSON=",dst/"verification.json")
sys.exit(v["status"]=="HOLD")
