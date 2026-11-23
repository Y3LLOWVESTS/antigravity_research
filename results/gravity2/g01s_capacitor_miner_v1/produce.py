"""G01-S, quadratic scalar activation in a finite, net-neutral spherical capacitor.

Einstein term, canonical dimensionless scalar phi with positive energy
K(|grad phi|^2+mu^2 phi^2)/2, K=c^4/(4 pi G), Maxwell factor
Z=exp(eta phi^2/2), material metric exp(b phi^2)g. SI fixed free charges +Q,-Q,
regular center and decaying exterior; electrostatic field vanishes outside R.
Conserved spherical electrode charges are an idealization. Ordinary photon:
alpha_EM/alpha_EM0=1/Z and Qe_A=d log(m_A)/d log(alpha_EM). In the local
constant-sensitivity approximation b_A=b-eta Qe_A. A species-independent
offset in Qe is absorbed in b. Hidden carrier: this electromagnetic binding
term may be absent, but physically sourced dark electrodes have to be derived.
At phi=0 both first derivatives vanish. G01-R's linear Yukawa limit cannot
be directly applied. Positive eta gives electric, not magnetic, activation.
"""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

G,C,g,R,BUDGET=6.67430e-11,299792458.,9.80665,2.,1.e7
CORE=.1
DENSITY=40/(23*2*np.pi**2*1*.2**2)
PARENT="results/gravity2/g01r_finite_range_miner_v1"
LOCKS={PARENT+"_UPLOAD.tar.gz":"d77a7a0eb70bab2d0f95e34f3ba8528d008d21785a0b7ff17754f7ee74cc0e52",
       PARENT+"/science.json":"650f6f582f5b4385c05feb0eede6b3ba4e1f241894823fa979e614df6aa0f392",
       PARENT+"/verification.json":"3001a19cff66b63ae0492970632725f58df838cc20035366a00a812c4a84d63b",
       PARENT+"/constraints.json":"37bc6a6dc0cd92174e9018701a70bc1c17bd9b33b0971a8bcfb15c41eceb4b44",
       "src/antigravity_research/agminer/hook17_f2_strong_payload_loading_rescue.py":
       "e1296794c25a4d0e4d5634c7e7d543a0b488b8d2a1963afcf7878bea1c1b99e7"}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def core_log_energy(logb,mu=0):
    b=np.exp(logb)
    x=CORE*np.sqrt(mu**2+4*np.pi*G*DENSITY*b/C**2)
    return np.log(C**2*CORE**2*g/G)-logb+2*(x+np.log(-np.expm1(-2*x))-np.log(2*x))

def threshold(mu,a,n):
    # t=(1/a-1/r)/(1/a-1/R) in [0,1]. At onset, -v''+(mu*delta*r^2)^2 v
    # = L*v. Positive surface Robin terms match core and exterior exactly.
    delta=1/a-1/R
    t=np.linspace(0,1,n+1)
    r=1/(1/a-delta*t)
    lo=0 if mu==0 else delta*a*(mu*a/np.tanh(mu*a)-1)
    hi=delta*R*(1+mu*R)
    diag=2.*n**2+np.square(mu*delta*r**2)
    diag[0]+=2*n*lo
    diag[-1]+=2*n*hi
    off=np.full(n,-float(n*n))
    off[[0,-1]]*=np.sqrt(2)
    val=eigh_tridiagonal(diag,off,select='i',select_range=(0,0),
                        eigvals_only=True,check_finite=False)[0]
    return val*C**4/(G*BUDGET*delta)

def main(root,out):
    for f,pin in LOCKS.items():
        if sha(root/f)!=pin: raise ValueError("immutable parent drift "+f)
    upper=np.exp(brentq(lambda l:core_log_energy(l)-np.log(BUDGET),np.log(1e27),np.log(1e32)))
    lower=np.exp(brentq(lambda l:core_log_energy(l)-np.log(BUDGET),np.log(1e15),np.log(1e23)))
    radii=np.linspace(.5,1.98,100)
    lengths=np.r_[np.inf,np.geomspace(.003,3000,241)]
    levels=[]
    for n in (32,64,128):
        eta=np.array([[threshold(1/length,a,n) for a in radii] for length in lengths])
        if not np.all(np.isfinite(eta)) or np.min(eta)<=0: raise ValueError("spectrum")
        levels.append(eta)
        print("radial mesh",n,"distinct parameter pairs",eta.size,"eta minimum",eta.min(),flush=True)
    # Sharpness of the flat-core mass feedback test independent of capacitor
    # details. By comparison on a core ball of radius h, |phi(0)| <=
    # x/sinh(x)*mean_boundary |phi|. The gradient energy outside the ball
    # is >=2*pi*K*h*mean_boundary(|phi|)^2 by raywise Cauchy-Schwarz.
    # Uniform +z acceleration to height h implies b_A*c^2*phi(0)^2/2>=g*h.
    # Use a permissive constant massless upper root for every range.
    delta_q=.00409-.00204
    exact_eta_floor=C**4*radii.min()/(G*BUDGET)
    mismatch=exact_eta_floor*delta_q/upper
    griderr=np.abs(levels[-1]/levels[-2]-1)
    at=np.unravel_index(levels[-1].argmin(),levels[-1].shape)
    doc=dict(experiment="G01-S",action=__doc__,parents=LOCKS,producer_sha256=sha(Path(__file__)),
       range_m=[None]+lengths[1:].tolist(),inner_radius_m=radii.tolist(),outer_radius_m=R,
       mesh_n=[32,64,128],eta_threshold_by_mesh=[v.tolist() for v in levels],
       count=len(radii)*len(lengths),range_span_expansion=(3000/.003)/(300/.03),
       per_cell_fractional_change=griderr.tolist(),count_change_over_1pct=int(np.sum(griderr>.01)),
       max_change=float(griderr.max()),minimum_grid_eta=float(levels[-1][at]),argmin=list(map(int,at)),
       action_curvatures="positive b_A exp(b_A phi^2/2) leading constant sensitivity; fixed density",
       load_profile="1 kg flat C1 torus, 1 m major and .2 m minor radius, .1 m constant-density core",
       core_density_kg_m3=DENSITY,positive_bA_necessary_window=[lower,upper],
       upper_abs_delta_Qe_to_fit=upper/exact_eta_floor,minimum_onset_eta_analytic=exact_eta_floor,
       delta_Qe_Ti_Pt=delta_q,minimum_interval_mismatch_factor=mismatch,
       reference="Damour & Donoghue arXiv:1007.2792 (dominant composition-dependent electromagnetic charges)",
       assumptions=["static nongravitational limit; no pre-existing scalar gradient",
        "generous 10 MJ limit for field energy or unscalarized capacitor charge-up considered separately",
        "native capacitor off-state spectral onset with nonnegative material Hessian; source-side walls omitted in atlas",
        "uniform positive acceleration for both test compositions in separate experiments of identical density",
        "ordinary-photon closure conditional on constant composition slopes at weak excursion; no independent cancellations",
        "no driven time-dependent branch, biased vacuum or negative-cost energy reservoir"],
       status="NECESSARY_CONDITION_ATLAS",physical_survivors=0,whole_craft="OPEN",full_regression="NOT_RUN")
    with (out/"science.json").open("x") as f: json.dump(doc,f,sort_keys=True,allow_nan=False)

if __name__=="__main__":
    main(*map(Path,sys.argv[1:3]))
