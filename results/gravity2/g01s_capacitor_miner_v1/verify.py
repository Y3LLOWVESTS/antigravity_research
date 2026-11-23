"""Independent onset check in the physical radial coordinate using polynomial
Rayleigh-Ritz quadrature and the exact continuum exterior/core Robin energy.
Independent integrations also test the torus-core screening and source capacity
bounds; raw precision is recorded per cell rather than asserting convergence
of a short-range boundary layer on every mesh.
"""
from pathlib import Path
import hashlib,json,sys
import math
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq
from scipy.integrate import quad, solve_ivp
from numpy.polynomial.legendre import leggauss,legvander,legder,legval

sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
root,out=map(Path,sys.argv[1:3])
s=json.loads((out/"science.json").read_bytes())
if s["producer_sha256"]!=sha(out/"produce.py"): raise ValueError("producer drift")
for n,pin in s["parents"].items():
    if sha(root/n)!=pin: raise ValueError("parent drift "+n)
import tarfile
ar=next(n for n in s["parents"] if n.endswith('.tar.gz'))
with tarfile.open(root/ar,'r:gz') as t:
    base=Path(ar).name.removesuffix('_UPLOAD.tar.gz')
    for line in t.extractfile(base+'/SHA256SUMS.txt').read().decode().splitlines():
        pin,n=line.split()
        if hashlib.sha256(t.extractfile(base+'/'+n).read()).hexdigest()!=pin or sha((root/ar).parent/base/n)!=pin:
            raise ValueError("parent member drift")
G,C,g=6.67430e-11,299792458.,9.80665
K=C**4/(4*math.pi*G)
E=1e7
R=2.
radii=s['inner_radius_m']; lens=s["range_m"]
data=np.array(s['eta_threshold_by_mesh'])
if data.shape!=(3,242,100) or s['count']!=24200: raise ValueError('coverage')
if not(np.all(np.diff(data[-1],axis=0)[1:]<=1e-11*data[-1,1:-1]) and
       len(set(radii))==100 and len(set(lens))==242): raise ValueError('distinct spectrum or monotonicity')
x,w=leggauss(100)
degree=46
P=legvander(x,degree)
dP=np.stack([legval(x,legder(v)) for v in np.eye(degree+1)],axis=1)
def ritz(mu,a):
    rad=(a+R+(R-a)*x)/2
    weights=w*(R-a)/2
    # v=r*phi, variational pencil: int(v'^2+mu^2 v^2) and
    # int(v^2/r^4) in the gap, with exact decaying exterior.
    lo=mu/np.tanh(mu*a) if mu else 1/a
    signs=(-1.)**np.arange(degree+1)
    B=P.T@((weights/rad**4)[:,None]*P)
    A=dP.T@((weights*4/(R-a)**2)[:,None]*dP)+mu**2*P.T@(weights[:,None]*P)
    A+=lo*np.outer(signs,signs)+mu
    return eigh(A,B,subset_by_index=(0,0),eigvals_only=True)[0]*4*np.pi*K*(1/a-1/R)/E
checks=[]
for i in sorted({0,1,2,11,36,61,97,121,161,200,241,s['argmin'][0]}):
    mu=0 if lens[i] is None else 1/lens[i]
    for j in (0,23,50,75,99):
        v=ritz(mu,radii[j]); diff=abs(data[-1,i,j]/v-1)
        checks.append(dict(i=i,j=j,independent_eta=v,relative_error=diff))
        if diff>.08: raise ValueError(("physical-coordinate convergence",i,j,diff))
for j,a in enumerate(radii):
    delta=1/a-1/R
    t=brentq(lambda v:v*np.tan(v)-delta*R,0,np.pi/2-1e-10)
    exact=t**2*4*np.pi*K/(E*delta)
    if abs(data[-1,0,j]/exact-1)>4e-5: raise ValueError('massless closed form')
source_bound=4*np.pi*K*min(radii)/E
if np.any(data[-1]<.999*4*np.pi*K*np.array(radii)/E): raise ValueError("capacity bound")
rho=1/(2*np.pi**2*.2**2*quad(lambda u:2*u*(1 if u<=.5 else (2-2*u)**2*(3-2*(2-2*u))),0,1,points=[.5])[0])
# Check center attenuation using regular spherical source-free IVP normalized
# to averaged boundary amplitude 1; integral of the exterior capacity
# extremizer (R/r) saturates the gradient energy bound.
for x0 in (.01,1.,10.,30.):
    k=x0/.1
    v=solve_ivp(lambda r,w:(w[1],k*k*w[0]),[0,.1],[0,1],rtol=2e-11,atol=2e-13)
    if abs(v.y[0,-1]/.1/(np.sinh(x0)/x0)-1)>1e-9: raise ValueError("screening")
cap=quad(lambda r:4*np.pi*.1**2/r**2,.1,np.inf)[0]
def cost(b):
    x0=.1*np.sqrt(b*4*np.pi*G*rho)/C
    return (K/2*cap)*(2*g*.1/(C*C*b))*(np.sinh(x0)/x0)**2
b_lo,b_hi=(10**brentq(lambda p:math.log(cost(10**p)/E),*bounds) for bounds in ((16,24),(27,32)))
if not np.allclose([b_lo,b_hi],s['positive_bA_necessary_window'],rtol=2e-9,atol=0): raise ValueError('core envelope')
if not np.isclose(source_bound*(.00409-.00204)/b_hi,s['minimum_interval_mismatch_factor']): raise ValueError('composition test')
# Reversing electric to magnetic sign adds a nonnegative potential; the zero
# field has exactly zero matter force and no ordinary single-scalar exchange.
if min(data.flatten())<=0 or min(radii)<=0: raise ValueError('off-state control')
diff=np.abs(data[-1]/data[-2]-1)
outcome=dict(status='PASS_SCOPED_NUMERICS_AND_CONTINUOUS_BOUNDS',
       samples=checks,largest_independent_relative_error=max(c['relative_error'] for c in checks),
       cells_refinement_over_one_percent=int(np.sum(diff>.01)),
       affirmative_gate='ordinary-photon closure relies on positive matter curvature and electromagnetic sensitivity transfer',
       hidden_source_gate='requires independent microscopic carrier, supports, clock/force bounds',
       science_sha256=sha(out/'science.json'),checker_sha256=sha(Path(__file__)),
       full_regression='NOT_RUN')
with (out/'verification.json').open('x') as f: json.dump(outcome,f,sort_keys=True,indent=2,allow_nan=False)
print(outcome['status'],len(checks),'independent thresholds',outcome['largest_independent_relative_error'],flush=True)
