"""Independent G01-Q check using spherical-interface matching and plane traction.
Does not import the producer. A four-coefficient scalar interface solve per
material eigenchannel replaces the producer's shell admittance. A repeated
image expansion replaces the coupled multipole solve. Integrate vacuum stress
on the ground by a radial quadrature and independently differentiate the
fixed-charge energy numerically. Axis points and distances are in units of R.
"""
from pathlib import Path
import hashlib,json,math,sys
import numpy as np
import mpmath as mp
from numpy.polynomial.legendre import leggauss
from scipy.special import eval_legendre,binom
mp.mp.dps=60
root,out,previous=map(Path,sys.argv[1:4])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
doc=json.loads((out/"science.json").read_bytes())
if (doc["producer_sha256"]!=sha(out/"produce.py")
    or doc["g01p_science_sha256"]!=sha(previous/"science.json")
    or doc["g01p_verification_sha256"]!=sha(previous/"verification.json")): raise ValueError("input drift")
parent=root/"results/gravity2/g01n_shell_source_v1/science.json"
if sha(parent)!=doc["g01n_science_sha256"]: raise ValueError("Run 2 drift")
rows=[r for r in json.loads(parent.read_bytes())["rows"] if r["eps_r"]==3.8]
def constitutive(z,p):
    return mp.matrix([[p+z*z,z],[z,1]])
def shell(r,N):
    z=mp.mpf(r["theta"])
    a=(1-mp.mpf(r["shell_fraction"]))**(mp.mpf(1)/3)
    eig,V=mp.eigsy(constitutive(z,mp.mpf(r["eps_r"])))
    blocks=[]
    for l in range(1,N+1):
        refl=[]
        for lam in eig:
            # core c r^l, shell b r^l + d r^(-l-1), exterior r^l + e r^(-l-1)
            t=a**(-2*l-1)
            mat=mp.matrix([[1,-1,-t,0],[l,-lam*l,lam*(l+1)*t,0],
                           [0,1,1,-1],[0,lam*l,-lam*(l+1),l+1]])
            refl.append(mp.lu_solve(mat,mp.matrix([0,0,1,l]))[3])
        block=V*mp.diag(refl)*V.T
        blocks.append(np.array(block.tolist(),dtype=float))
    return np.array(blocks)
def ground(r,kind):
    if kind=="conductor": return np.diag([-1.,0.])
    if kind=="vacuum": return np.zeros((2,2))
    M=constitutive(mp.mpf(r["theta"])*2000/2200,4)
    return np.array(((mp.eye(2)+M)**-1*(mp.eye(2)-M)).tolist(),dtype=float)
def iterate(H,S,B):
    N=len(S)
    l=np.arange(1,N+1)
    total=l[:,None]+l[None,:]
    shift=(-1.)**total*binom(total,l[:,None])/(2*H)**(total+1)
    free=np.zeros((N,2));free[0]=[1,-1]
    w=free.copy()
    for _ in range(250):
        inc=shift@(w@B.T)
        new=free+np.einsum("lij,lj->li",S,inc)
        if np.max(abs(new-w))<3e-15: break
        w=new
    else: raise ValueError("image iteration failed")
    return w,inc[0,0]-inc[0,1]
def traction(H,w,B,Ue,count):
    # mu here is positive, equal to H/r; cos(theta_sphere)=-mu on the plane.
    x,weight=leggauss(count)
    mu=(1+x)/2
    rad=H/mu; cosine=-mu
    normal=np.zeros((count,2)); tangent=normal.copy()
    for l,term in enumerate(w,1):
        P=eval_legendre(l+1,cosine)
        dp=(l+1)*(eval_legendre(l,cosine)-cosine*P)/(1-cosine**2)
        normal-=np.outer((l+1)*P/rad**(l+2),term)
        tangent-=np.outer(np.sqrt(1-cosine*cosine)*dp/rad**(l+2),term)
    # Each one-sided self-field has exactly zero integrated traction on
    # the plane (close the surface in the opposite empty half-space).
    # Integrate the cross stress directly, preserving the exact vacuum null.
    cross=-2*(np.sum(normal*(normal@B.T),axis=1)+np.sum(tangent*(tangent@B.T),axis=1))
    integrand=cross*H**2/mu**3
    return (3*Ue/(4*2))*np.dot(weight/2,integrand)
checks=[]
for r in rows:
    S=shell(r,48)
    Ue=r["exterior_electric_dipole_J"]
    for kind in ("conductor","dielectric","vacuum"):
        B=ground(r,kind)
        for gap in (.25,.5,1.,2.):
            H=1+gap/2
            w,_=iterate(H,S,B)
            fg=traction(H,w,B,Ue,96)
            low=traction(H,w,B,Ue,64)
            step=1e-4
            e=[iterate(H+j*step/2,S,B)[1]*1.5*Ue for j in (-2,-1,1,2)]
            fd=-(e[0]-8*e[1]+8*e[2]-e[3])/(12*step)
            hist=[e for e in doc["rows"] if e["kind"]==kind and
                  e["scale_eV"]==r["scale_eV"] and e["gap_m"]==gap]
            fc=hist[-1]["craft_field_force_up_N"]
            if [e["order"] for e in hist]!=[6,12,24,40]: raise ValueError("order inventory")
            tol=2e-8*max(abs(fc),1.e-3)
            if max(abs(fc+fg),abs(fc-fd),abs(fg-low))>tol: raise ValueError(("force audit",kind,gap,fc,fg,fd,low))
            if abs(hist[-2]["craft_field_force_up_N"]-fc)>1.e-4*max(1.e-3,abs(fc)):
                raise ValueError("truncation sensitivity")
            if kind=="conductor" and fc>=0: raise ValueError("conductor sign")
            checks.append(dict(scale_eV=r["scale_eV"],kind=kind,gap_m=gap,
                craft_up_N=fc,ground_up_traction_N=float(fg),
                translation_residual_N=float(fc+fg),finite_difference_up_N=float(fd),
                weight_N=hist[-1]["shell_weight_N"],ground_quadrature_change_N=float(abs(fg-low))))
if len(checks)!=24: raise ValueError("coverage")
doc=dict(status="PASS_SCOPED_RECIPROCAL_CARRIER_FORCE",checks=checks,
    largest_up_fraction=max(row["craft_up_N"]/row["weight_N"] for row in checks),
    science_sha256=sha(out/"science.json"),verifier_sha256=sha(Path(__file__)),
    whole_craft_hover=False,einstein_solution=False,full_regression="NOT_RUN")
with (out/"verification.json").open("x") as f: json.dump(doc,f,sort_keys=True,indent=2,allow_nan=False)
print(doc["status"],"largest_up_fraction",doc["largest_up_fraction"])
print("VERIFICATION_SHA256",sha(out/"verification.json"))
