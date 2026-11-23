"""Independent force calculation by Maxwell-stress integration and successive reflection.
Shares only the producer's panel inventory. Distances are in micrometres.
"""
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json,math,sys
import numpy as np
from scipy.special import lpmv,gammaln
from scipy.linalg import lu_factor,lu_solve
from numpy.polynomial.legendre import leggauss

root,out=map(Path,sys.argv[1:3])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
doc=json.loads((out/"science.json").read_bytes())
if sha(out/"produce.py")!=doc["producer_sha256"]: raise ValueError("producer drift")
for name,pin in doc["parents"].items():
    if sha(root/name)!=pin: raise ValueError("parent drift")
spec=spec_from_file_location("geometry",out/"produce.py")
geometry=module_from_spec(spec)
spec.loader.exec_module(geometry)
p=geometry.panels(2)
centers=np.zeros((len(p),3))
for i,(axis,h,x0,x1,y0,y1,_) in enumerate(p):
    j=int(axis)
    centers[i,[j,(j+1)%3,(j+2)%3]]=[h,(x0+x1)/2,(y0+y1)/2]

def green(points):
    result=np.zeros((len(points),len(p)))
    for j in range(3):
        sel=p[:,0]==j
        _,h,x0,x1,y0,y1,_=p[sel].T
        z=abs(points[:,j,None]-h)
        for x,signx in [(x0,-1),(x1,1)]:
            for y,signy in [(y0,-1),(y1,1)]:
                u=x-points[:,(j+1)%3,None]
                v=y-points[:,(j+2)%3,None]
                r=np.sqrt(u*u+v*v+z*z)
                # x log(r+y) primitive, using the conjugate at negative y
                def logplus(r,v,other):
                    tiny=1e-200
                    return np.where(v>=0,np.log(np.maximum(r+v,tiny)),
                              np.log(np.maximum(other**2+z*z,tiny))-np.log(np.maximum(r-v,tiny)))
                val=u*logplus(r,v,u)+v*logplus(r,u,v)-z*np.arctan2(u*v,z*r)
                result[:,sel]+=signx*signy*val/((x1-x0)*(y1-y0))
    return result

orders=[(l,m) for l in range(1,5) for m in range(0,l+1,2)]
L=np.array([l for l,m in orders])
def harmonic(vec):
    r=np.linalg.norm(vec,axis=1)
    mu=vec[:,2]/r
    phi=np.arctan2(vec[:,1],vec[:,0])
    return np.stack([np.sqrt((2*l+1)/(4*np.pi)*np.exp(gammaln(l-m+1)-gammaln(l+m+1))*(1+(m>0)))
        *lpmv(m,l,mu)*np.cos(m*phi) for l,m in orders],axis=1)

x,w=leggauss(11)
az=np.arange(24)*np.pi/12
mu,ph=np.meshgrid(x,az,indexing="ij")
directions=np.c_[(np.sqrt(1-mu**2)*np.cos(ph)).ravel(),(np.sqrt(1-mu**2)*np.sin(ph)).ravel(),mu.ravel()]
weights=np.repeat(w,24)*np.pi/12
project=harmonic(directions).T*weights
lu=lu_factor(green(centers))
q0=lu_solve(lu,p[:,6])
errors=[]
def test(d,a,theta):
    origin=np.array([0,0,d])
    scale=(a/np.linalg.norm(centers-origin,axis=1)[:,None])**(L+1)
    S=harmonic(centers-origin)*scale
    T=project@green(origin+a*directions)
    # Response from the inverse of the full 2x2 material matching matrix.
    # Stable form for the bright entry of the inverse, determinant expanded.
    K=1-(2*L+1)**2/((2*L+1)*(L*3.8+L+1)+L*(L+1)*theta**2)
    charge=q0.copy()
    for _ in range(8):
        scattered=-K*(T@charge)
        charge=lu_solve(lu,p[:,6]-S@scattered)
    scattered=-K*(T@charge)
    b=1.6*a
    v=b*directions
    def potential(v):
        return (harmonic(v)*(a/np.linalg.norm(v,axis=1)[:,None])**(L+1))@scattered
    inc=[]; sc=[]
    for axis in np.eye(3)*.008:
        inc.append(-((green(origin+v+axis)-green(origin+v-axis))@charge)/.016)
        sc.append(-(potential(v+axis)-potential(v-axis))/.016)
    e=np.array(inc).T
    u=np.array(sc).T
    integ=(e[:,2]*(u*directions).sum(1)+u[:,2]*(e*directions).sum(1)
           -directions[:,2]*(e*u).sum(1))
    force=b*b*np.dot(weights,integ)/(4*np.pi)
    h=.16
    phi=green(origin+np.outer(np.arange(-2,3)*h,[0,0,1]))@q0
    d1=(phi[0]-8*phi[1]+8*phi[3]-phi[4])/(12*h)
    d2=(-phi[0]+16*phi[1]-30*phi[2]+16*phi[3]-phi[4])/(12*h*h)
    return force/(a**3*K[0]*d1*d2)
for row in doc["samples"]:
    if row["level"]!=2: continue
    for obs in row["samples"]:
        if obs["distance_um"] not in (20,60) or obs["radius_um"]!=3.22: continue
        z=json.loads((root/"results/gravity2/g01o_static_source_overlap_v1/science.json").read_bytes())
        theta=next(t["theta"] for t in z["rows"] if t["portal_scale_eV"]==row["scale_eV"])
        calc=test(obs["distance_um"],obs["radius_um"],theta)
        errors.append(abs(calc-obs["force_ratios_L1_L2_L4"][-1]))
if len(errors)!=4 or max(errors)>.001: raise ValueError(("force check",errors))
ranges=[]
for row in doc["samples"]:
    vals=[v["force_ratios_L1_L2_L4"][-1] for v in row["samples"]]
    ranges.append([row["level"],row["scale_eV"],min(vals),max(vals)])
if len(ranges)!=6 or min(r[2] for r in ranges)<.98: raise ValueError("review transfer")
report=dict(status="VERIFIED_IDEAL_ELECTRODE_BRIGHT_LIMIT",max_force_ratio_error=max(errors),
     ranges=ranges,science_sha256=sha(out/"science.json"),verifier_sha256=sha(Path(__file__)),
     actual_apparatus_exclusion=False,full_regression="NOT_RUN")
with (out/"verification.json").open("x") as f: json.dump(report,f,sort_keys=True,indent=2)
print(report)
print("VERIFICATION_SHA256",sha(out/"verification.json"))
