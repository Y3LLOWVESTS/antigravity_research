"""Independent G01-R audit: infinite-domain Yukawa Green integral, gradient
energy integral, constrained orientation optimizer, and 1-D ground convolution.
Reads producer JSON; never imports the producer or its numerical implementation.
"""
import hashlib
import json
from math import pi
from pathlib import Path
import sys
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize
from scipy.special import ive,kve

root,out=map(Path,sys.argv[1:3])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
doc=json.loads((out/"science.json").read_bytes())
if sha(out/"produce.py")!=doc["producer_sha256"]: raise ValueError("source drift")
for path,expected in doc["parents"].items():
    if sha(root/path)!=expected: raise ValueError("parent drift "+path)
G=6.67430e-11
R=2.
g=9.80665
def check(ok,reason):
    if not ok: raise ValueError(reason)

def rule(edges,n):
    x,w=np.polynomial.legendre.leggauss(n)
    return fixed(np.unique(edges),x,w)

def fixed(edges,x,w):
    mid=(edges[:-1]+edges[1:])/2
    half=np.diff(edges)/2
    return (mid[:,None]+half[:,None]*x).ravel(),(half[:,None]*w).ravel()

gx,gw=np.polynomial.legendre.leggauss(18)
def vacuum(r,l):
    if l==0 and r<=R: return r*r/3-R*R/2,2*r/3
    if l==0: return -R**6/(6*r**4),2*R**6/(3*r**5)
    if r<=R: return r*r/30,r/15
    return R**5/(5*r**3)-R**6/(6*r**4),-3*R**5/(5*r**4)+2*R**6/(3*r**5)

def green(r,mu,l):
    if mu==0: return vacuum(r,l)
    # Split on the source jump and on the Green derivative jump. Include
    # geometrically spaced shells and Yukawa-scale nodes for each integral.
    limit=r+50/mu
    scales=r+np.array([-48,-16,-4,-1,0,1,4,16,48])/mu
    knots=np.unique(np.clip(np.r_[0.,R,r,limit,scales,
                     np.geomspace(.03,max(.04,limit),30)],0,limit))
    t,w=fixed(knots,gx,gw)
    nu=l+.5
    lo=np.minimum(t,r)*mu
    hi=np.maximum(t,r)*mu
    kern=ive(nu,lo)*kve(nu,hi)*np.exp(lo-hi)/np.sqrt(t*r)
    inside=t<r
    slope=np.where(inside,-mu*kve(nu+1,mu*r)/kve(nu,mu*r)+l/r,
                    mu*ive(nu+1,mu*r)/ive(nu,mu*r)+l/r)
    source=np.where(t<R,(-2. if l==0 else 0.),(2. if l==0 else 1.)*(R/t)**6)
    terms=w*t*t*source*kern
    return np.sum(terms),np.sum(terms*slope)

def plane(mu,H):
    # Integrate the physical dipole's E.B over each horizontal slice first.
    def zsource(z):
        if abs(z)<R: return pi*R**2*(-1.5+3*(z/R)**2)
        return 1.5*pi*R**6/z**4
    def kernel(z):
        h=abs(H+z)
        return -h if mu==0 else np.expm1(-mu*h)/mu
    edges=(-np.inf,-H,-R,R,np.inf)
    total=sum(quad(lambda z:zsource(z)*kernel(z),a,b,epsabs=2e-10,epsrel=1e-10)[0]
              for a,b in zip(edges,edges[1:]))
    return 1000*total

def norms_and_grads(mu):
    part=[0,R,5,*np.geomspace(.01,8192,65)]
    if mu: part.extend(max(0,min(8192,R+j/mu)) for j in (-8,-1,-.2,.2,1,8))
    rad,w=rule(part,8)
    t=np.linspace(0,2*pi,281,endpoint=False)
    s=np.linspace(0,.2,37)[:,None]
    z=np.sqrt((2+1+.2)**2-1)+s*np.sin(t)
    rr=np.hypot(1+s*np.cos(t),z).ravel()
    ct=z.ravel()/rr
    xs=np.linspace(2.999,3.401,65)
    d=[];cost=[]
    for l in (0,2):
        vals=np.array([green(x,mu,l) for x in rad])
        energy=np.dot(w,rad**2*vals[:,1]**2+(l*(l+1)+(mu*rad)**2)*vals[:,0]**2)
        cost.append(energy/(2*G*(2*l+1)))
        vals=np.array([green(x,mu,l) for x in xs])
        f,df=CubicSpline(xs,vals,axis=0)(rr).T
        d.append(-ct*df if l==0 else -df*ct*(3*ct**2-1)/2-f*3*ct*(1-ct**2)/rr)
    return np.column_stack(d),np.array(cost)

def optimum(d,cost):
    A=d/np.sqrt(cost)
    scale=np.max(abs(A))
    A=A/scale
    # Collapse repeated constraints by using the active-set method:
    # insert the currently worst violated sample until all are feasible.
    active=[0]
    x=np.zeros(2)
    for _ in range(30):
        sub=A[active]
        result=minimize(lambda u:.5*np.dot(u,u),x,jac=lambda u:u,
                   constraints=[dict(type="ineq",fun=lambda u:sub@u-1,jac=lambda u:sub)],
                   method="SLSQP",options={"ftol":1e-13,"maxiter":250})
        x=result.x
        worst=np.argmin(A@x)
        if min(A@x)>1-2e-9: return (g/scale)**2*np.dot(x,x)
        if worst in active: return None
        active.append(worst)
    raise ValueError("independent optimizer did not settle")

levels=doc["levels"]
check([e["n"] for e in levels]==[96,192,384],"mesh inventory")
mus=np.r_[0,1/np.geomspace(300,.03,241)]
for level in levels:
    check(len(level["rows"])==242,"range coverage")
    check(np.allclose([r["mu_per_m"] for r in level["rows"]],mus,rtol=2e-15,atol=0),"mass inventory")
    for row in level["rows"]:
        check(min(row["energy_norms"])>0,"positive canonical energy")
        if row["axial"] is not None:
            check(row["relaxed"] is not None and row["relaxed"][0]<=1.00001*row["axial"]["alpha2_energy_J"],"relaxation")
fine=levels[-1]["rows"]
okay=[(r["relaxed"][0],i) for i,r in enumerate(fine) if r["relaxed"] is not None]
best,index=min(okay)
best_axis=min((r["axial"]["alpha2_energy_J"],i) for i,r in enumerate(fine) if r["axial"] is not None)
target=g*g*(2*pi**2*.2**2)/(8*pi*G)
check(abs(target/doc["target_volume_alpha2_energy_floor_J"]-1)<1e-12,"finite payload bound")
check(best>target,"implausible torus lower bound")
# All stored rows: finite-volume stability across last two resolutions,
# including range-by-range sign classification. Flag near-transition flips.
relative=[]
flips=[]
for i,(a,b) in enumerate(zip(levels[-2]["rows"],fine)):
    if (a["relaxed"] is None)!=(b["relaxed"] is None) or (a["axial"] is None)!=(b["axial"] is None):
        flips.append(i)
    if a["relaxed"] and b["relaxed"]:
        relative.append(abs(a["relaxed"][0]/b["relaxed"][0]-1))
checks=[]
indices=sorted({0,1,31,61,91,121,151,181,211,241,index,best_axis[1]})
for i in indices:
    row=fine[i]; mu=row["mu_per_m"]
    d,cost=norms_and_grads(mu)
    rel=np.max(np.abs(cost/np.array(row["energy_norms"])-1))
    check(rel<.003,("energy quadrature",i,rel))
    indep=optimum(d,cost)
    check((indep is None)==(row["relaxed"] is None),("independent sign",i))
    gap=None if indep is None else abs(indep/row["relaxed"][0]-1)
    check(gap is None or gap<.008,("independent minimum",i,gap))
    axis=d[:,0]+2*d[:,1]
    check(np.max(abs(np.array([min(axis),max(axis)])-row["raw_axial_range"]))/max(abs(axis))<.001,
          ("dipole sign or force normalization",i))
    axial=row["axial"]
    ground_gap=None
    if axial:
        ref=np.array([plane(mu,2+h) for h in (.25,.5,1,2)])*axial["coeff"]
        vals=axial["ground_reaction_craft_up_N"]
        ground_gap=max(abs(vals-ref))/max(1,max(abs(ref)))
        check(ground_gap<.003,("reciprocal ground force",i,ground_gap))
    checks.append(dict(i=i,mu=mu,relative_energy_norm_error=rel,relative_optimum_error=gap,
                       relative_ground_error=ground_gap))
# Independent controls: integrated E.B, applied-source reversal, no drive,
# angular averaging versus rotated dipoles, Yukawa-to-Poisson continuity.
p=np.array([.36,.48,.8]); m=np.array([-.8,0,.6])
angle=np.arange(128)*2*pi/128
c=.27
nhat=np.column_stack([np.sqrt(1-c*c)*np.cos(angle),np.sqrt(1-c*c)*np.sin(angle),np.full(128,c)])
cross=(p@m)+3*(nhat@p)*(nhat@m)
proj=2*(p@m)+(3*p[2]*m[2]-p@m)*(3*c*c-1)/2
check(abs(np.mean(cross)-proj)<1e-14,"rotation")
check(max(abs(cross+((-p)@m+3*(nhat@(-p))*(nhat@m))))<1e-14,"polarity")
check(np.max(abs(nhat@np.zeros(3)))==0,"null drive")
check(abs(-2*R**3/3+quad(lambda r:2*R**6/r**4,R,np.inf)[0])<1e-12,"monopole")
for l in (0,2):
    check(max(abs(np.array(green(3.15,1e-6,l))-vacuum(3.15,l)))<2e-5,"massless limit")
status="PASS_SCOPED" if max(relative)<.01 and not flips else "HOLD_GRID_SENSITIVE_ROWS"
report=dict(status=status,independent_checks=checks,range_count=len(mus),bounded_relaxed_rows=len(okay),
    axial_uniform_sampled_rows=sum(r["axial"] is not None for r in fine),
    minimum_relaxed_alpha2_energy_J=best,best_relaxed_index=index,minimum_axial_alpha2_energy_J=best_axis[0],
    best_axial_index=best_axis[1],max_refinement_relative_energy=max(relative),sign_classification_changes=flips,
    target_only_alpha2_energy_J=target,controls=["null","polarity","integrated monopole","rotated fields","massless"],
    science_sha256=sha(out/"science.json"),checker_sha256=sha(Path(__file__)),full_regression="NOT_RUN",
    physical_survivors=0,loaded_free_torus="NOT_SOLVED",complete_energy="NOT_CERTIFIED")
with (out/"verification.json").open("x") as f: json.dump(report,f,sort_keys=True,indent=2,allow_nan=False)
print(status,"range rows",len(mus),"relaxed",len(okay),"axial",report["axial_uniform_sampled_rows"])
print("alpha squared times energy, minimum relaxed / axial / volume",best,best_axis[0],target)
print("grid drift",max(relative),"sign changes",flips)
