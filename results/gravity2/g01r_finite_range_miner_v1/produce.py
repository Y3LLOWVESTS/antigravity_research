"""G01-R: static linear-response limit of a finite-range mixed-field portal.

One ordinary Maxwell field is realized by taking the two canonical U(1)s
in the same bright direction (the orthogonal combination has zero off-state
drive). Absorb the projection factor into eta. In -+++ conventions use
EH, a canonical dimensionless scalar with energy K/2[(grad phi)^2+mu^2 phi^2],
K=c^4/(4 pi G), a Maxwell term and the topological coupling with static
L_int=eta phi epsilon0 E.cB. Ordinary matter couples to exp(2 alpha phi)g.
Free shell surface charge ~p.n and circulating current ~m cross n are
separately conserved static Maxwell dipole sources. Physical charge carriers,
retention, supports, a material law and full Einstein equations are open.
Source-/off-state subtraction holds only at fixed material density at this
linear order. D and H depend on eta phi, so strong feedback requires a new
coupled solution. This is neither the historical R3B action nor a QCD axion.

For unit dipoles E/e and cB/b outside are (3 n n^T-I)p,m times (R/r)^3.
Inside they are -p and 2m. For independent axes the azimuthal average of
E.cB / (e b) is A*s0+B*s2*P2, A=p.m, B=2*pz*mz-p_perp.m_perp.
s0=-2 inside and 2(R/r)^6 outside; s2=0 inside and (R/r)^6 outside.
Include the exterior source all the way to the radial boundary. The angular
monopole integrates to zero exactly, by int grad(V).B = boundary flux.
Allow arbitrary real A,B after normalization: necessary relaxation of
any pair of dipoles. Omitted azimuthal harmonics cost positive energy.
For axial dipoles B=2A is physical; reverse either drive for the other sign.

Define the scalar potential per unit mass Psi=alpha*c^2*phi. Its two radial
bases solve (-Delta+mu^2)f_l=s_l, regular at zero, vanishing at infinity.
Coefficient units are s^-2. Force means the differential +z acceleration
on fixed neutral matter when switching the drives. Scalar-field energy is
int [(grad Psi)^2+mu^2 Psi^2]/(8*pi*G*alpha^2). Ground is a frozen half-
space transparent to the applied EM field, density 2000 kg/m^3; only the
switch-correlated scalar exchange is included. Force on source system
equals +rho int_plane Psi dA, opposite the volume force on ground.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import solve_banded
from scipy.spatial import ConvexHull

G, C, R, TARGET = 6.67430e-11, 299792458., 2., 9.80665
BUDGET = 1e7
GAPS = (0.25, 0.5, 1., 2.)
PINS = {
    "results/data/032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json":
    "9474b6782104abb5bd8dd5e893137621b30ad96109e3e52c5a01268794810b11",
    "results/gravity2/g01q_shell_ground_reaction_v1/science.json":
    "11c38bdb06246a004b32f3a71e8f589a4d546a936d07979f1be4f585317efe4b",
    "src/antigravity_research/gravity2/engine.py":
    "17f83c04ec069a56e5a678240051cbe18589398bde06de6dafb7c64d81f6fae6",
    "src/antigravity_research/gravity2/policy.py":
    "e35aeb28d11fa5621d7767c53698ca614b1fa99b4efd717a415cb2d32cb6c25c",
}
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def torus(n):
    theta = np.arange(4*n)*np.pi/(2*n)
    radius = np.linspace(0, .2, n//2+1)[:, None]
    x = (1+radius*np.cos(theta)).ravel()
    z = (np.sqrt(3.2**2-1)+radius*np.sin(theta)).ravel()
    rad = np.hypot(x,z)
    return rad,z/rad

def fem_mesh(n):
    # Nodes include the source jump, all four plane cutoffs, and torus region.
    r = np.unique(np.r_[np.linspace(0,2,n+1), np.linspace(2,6,2*n+1),
                        np.geomspace(6,16384,3*n+1),[R+g for g in GAPS]])
    left, h = r[:-1], np.diff(r)
    xi, wi = np.polynomial.legendre.leggauss(4)
    shape=np.stack(((1-xi)/2,(1+xi)/2))
    x=left[:,None]+h[:,None]*shape[1]
    w=h[:,None]*wi/2
    return r,h,x,w,shape

def radial(mesh,mu,l):
    r,h,x,w,N = mesh
    potential=mu**2 + l*(l+1)/x**2
    force=np.where(x<R,-2. if l==0 else 0.,(2. if l==0 else 1.)*(R/x)**6)
    mass=w*potential
    d0=1/h+mass@(N[0]**2)
    d1=1/h+mass@(N[1]**2)
    off=-1/h+mass@(N[0]*N[1])
    diag=d1[:-1]+d0[1:]
    load=w*x*force
    rhs=(load@N[1])[:-1]+(load@N[0])[1:]
    ab=np.zeros((3,len(diag)))
    ab[0,1:]=off[1:-1]
    ab[1]=diag
    ab[2,:-1]=off[1:-1]
    v=np.r_[0,solve_banded((1,1),ab,rhs),0]
    integral=np.dot(v[1:-1],rhs)
    f=CubicSpline(r[1:],v[1:]/r[1:])
    plane=[]
    for gap in GAPS:
        H=R+gap
        live=r[:-1]>=H
        y=x[live]
        angular=1 if l==0 else (3*(H/y)**2-1)/2
        plane.append(float(2*np.pi*2000*np.sum(w[live]*y*f(y)*angular)))
    return f, integral/(2*G*(2*l+1)), plane

def relax(d,energies):
    # In energy-whitened coefficient space the nearest point of the convex
    # hull of all sample gradients gives the exact worst-case optimum.
    z=d/np.sqrt(energies)
    scale=np.max(abs(z))
    z=z/scale
    hull=ConvexHull(z)
    if np.all(hull.equations[:,-1] <= 0):
        return None
    a=z[hull.vertices]
    vec=np.roll(a,-1,axis=0)-a
    frac=np.clip(-np.sum(a*vec,axis=1)/np.sum(vec*vec,axis=1),0,1)
    points=a+frac[:,None]*vec
    point=points[np.argmin(np.sum(points**2,axis=1))]
    coeff=TARGET*point/(scale*np.dot(point,point)*np.sqrt(energies))
    if abs(min(d@coeff)-TARGET)>1e-6:
        raise ValueError("orientation optimizer residual")
    return float(energies@coeff**2),coeff.tolist()

def trial(mesh,loc,mu):
    rr,t=loc
    angular=(3*t**2-1)/2
    functions=[]; costs=[]; surfaces=[]
    for l in (0,2):
        f,cost,plane=radial(mesh,mu,l)
        grad=(t*f(rr,1) if l==0 else
              t*f(rr,1)*angular+3*t*(1-t*t)*f(rr)/rr)
        functions.append(-grad)
        costs.append(cost)
        surfaces.append(plane)
    d=np.column_stack(functions)
    costs=np.array(costs)
    best=relax(d,costs)
    axis=d[:,0]+2*d[:,1]
    choices=(min(axis),-max(axis))
    axial=None
    if max(choices)>0:
        coef=TARGET/max(choices)*(1 if choices[0]>choices[1] else -1)
        energy=coef**2*(costs[0]+4*costs[1])
        forces=coef*(np.array(surfaces[0])+2*np.array(surfaces[1]))
        axial=dict(coeff=float(coef),alpha2_energy_J=float(energy),
                   ground_reaction_craft_up_N=forces.tolist(),
                   minimum_abs_alpha_eta_if_EM_below_10MJ=float(abs(coef)*np.sqrt(2)*R**3*C**2/(G*BUDGET)))
    return dict(mu_per_m=mu,energy_norms=costs.tolist(),raw_axial_range=[float(min(axis)),float(max(axis))],
                relaxed=best,axial=axial)

def main(root,out):
    for name,pin in PINS.items():
        if sha(root/name)!=pin: raise ValueError("parent drift "+name)
    mus=np.r_[0,1/np.geomspace(300,.03,241)]
    levels=[]
    for n in (96,192,384):
        mesh=fem_mesh(n)
        loc=torus({96:16,192:32,384:64}[n])
        results=[trial(mesh,loc,float(mu)) for mu in mus]
        print("mesh",n,"ranges",len(results),"payload samples",len(loc[0]),flush=True)
        levels.append(dict(n=n,samples=len(loc[0]),rows=results))
    doc=dict(run="G01-R",producer_sha256=sha(Path(__file__)),parents=PINS,
       geometry=dict(shell_radius_m=R,torus_major_m=1.,torus_minor_m=.2,payload_mass_kg=1.,
                     standoff_m=1.,ground_gaps_m=GAPS,ground_density_kg_m3=2000),
       assumptions=__doc__,levels=levels,research_status="NECESSARY_CONDITION_AND_FIRST_ORDER_RESPONSE",
       target_volume_alpha2_energy_floor_J=TARGET**2*(2*np.pi**2*.2**2)/(8*np.pi*G),
       references=["10.1103/PhysRevD.32.3084","10.1103/PhysRevLett.58.1799"],
       complete_energy="UNCERTIFIED",physical_survivors=0,full_regression="NOT_RUN")
    with (out/"science.json").open("x") as f: json.dump(doc,f,sort_keys=True,allow_nan=False)
    print("science_sha256",sha(out/"science.json"),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("root",type=Path); p.add_argument("out",type=Path)
    args=p.parse_args()
    main(args.root,args.out)
