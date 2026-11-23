"""G01-Q. Fixed free surface charge on the G01-N, s=1 shell over a planar substrate.

The linear static field equations in each homogeneous region admit harmonic
potentials (phi_X, psi_HY). Use G01-N's weak-trace coefficient and its
measured-in-the-model shell fraction. Keep the free dipolar charge fixed
while all induced multipoles relax at each separation. No free Y drive.
The reference dipole is normalized in the isolated geometry only.
The ground is an infinite half-space in vacuum, either a frozen uniform
dielectric (assumed rho=2000 kg/m^3 and eps=4) or an equilibrated ideal
bright conductor transparent to hidden magnetism. Ambient Earth gravity
enters only as shell weight. No Einstein/Earth interior solution, torus,
mechanical source completion, support/retention or empirical certification.
"""
from pathlib import Path
from math import comb
import json,hashlib,sys
import numpy as np

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def reflection(kind,theta):
    if kind=="vacuum": return np.zeros((2,2))
    if kind=="conductor": return np.diag([-1.,0.])
    if kind!="dielectric": raise ValueError("unknown substrate")
    eps=4.
    z=theta*2000/2200
    return np.array([[2-2*eps-z*z,-2*z],[-2*z,z*z]])/(2+2*eps+z*z)

def shell_blocks(N,z,p,f):
    # Stable eigenvalues: det(M)=p even at the 1 keV contrast.
    angle=.5*np.arctan2(2*z,p+z*z-1)
    basis=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    large=.5*(1+p+z*z+np.hypot(2*z,p+z*z-1))
    eig=np.array([large,p/large])
    blocks=[]
    for l in range(1,N+1):
        t=-np.expm1((2*l+1)*np.log1p(-f)/3)
        Y=l*eig*((2*l+1)+(l+1)*(eig-1)*t)/((2*l+1)*eig-l*(eig-1)*t)
        blocks.append((basis*((l-Y)/(l+1+Y)))@basis.T)
    return np.array(blocks)

def solve(row,kind,gap,N):
    R=2.
    d=2*(R+gap)/R
    ind=np.arange(1,N+1)
    powers=ind[:,None]+ind[None,:]+1
    translation=np.array([[(-1.)**(l+k)*comb(l+k,l)/d**(l+k+1)
        for k in range(1,N+1)] for l in range(1,N+1)])
    refl=reflection(kind,row["theta"])
    T=np.kron(translation,refl)
    Td=np.kron(-powers*translation*2/(R*d),refl)
    blocks=shell_blocks(N,row["theta"],row["eps_r"],row["shell_fraction"])
    S=np.zeros_like(T)
    for i,block in enumerate(blocks):
        S[2*i:2*i+2,2*i:2*i+2]=block
    fixed=np.zeros(2*N)
    fixed[:2]=[1.,-1.]
    A=np.eye(2*N)-S@T
    w=np.linalg.solve(A,fixed)
    dw=np.linalg.solve(A,S@Td@w)
    inc=T@w
    derivative=Td@w+T@dw
    # Fixed-charge energy change is 1/2 integral sigma_free delta(phi).
    # Dipole reciprocity: Q_1^T (I+S_1) = 3 w0_1^T in R-normalized units.
    Ue=row["exterior_electric_dipole_J"]
    energy=1.5*Ue*(inc[0]-inc[1])
    force=-1.5*Ue*(derivative[0]-derivative[1])
    residual=float(np.max(abs(A@w-fixed)))
    return dict(order=N,gap_m=gap,kind=kind,interaction_J=float(energy),
        craft_field_force_up_N=float(force),shell_weight_N=row["shell_mass_kg"]*9.80665,
        fraction_shell_weight=float(force/(row["shell_mass_kg"]*9.80665)),residual=residual,
        loaded_exterior_dipole=w[:2].tolist())

def main(root,out,previous):
    n=root/"results/gravity2/g01n_shell_source_v1/science.json"
    pins={n:"7635896c65e47e64ffa772651a55605e38499790b44a7c37a582c537a8c752fb",
       previous/"produce.py":"d07f67e5382388a0b3008ff37ed805783f6fac410d45396ce1437e1c96589242",
       previous/"verify.py":"7b907d997ffc1653455a8771d88e1c1dd28219eaab8c6239dac9ce6ac7ce2776"}
    for path,pin in pins.items():
        if sha(path)!=pin: raise ValueError("parent drift "+str(path))
    prev=json.loads((previous/"science.json").read_bytes())
    verify=json.loads((previous/"verification.json").read_bytes())
    if (verify["science_sha256"]!=sha(previous/"science.json")
        or verify["status"]!="VERIFIED_IDEAL_ELECTRODE_BRIGHT_LIMIT"
        or prev["producer_sha256"]!=sha(previous/"produce.py")
        or verify["verifier_sha256"]!=sha(previous/"verify.py")): raise ValueError("Run 4 hold")
    rows=[]
    for r in json.loads(n.read_bytes())["rows"]:
        if r["eps_r"]!=3.8: continue
        for N in (6,12,24,40):
            for kind in ("vacuum","conductor","dielectric"):
                for gap in (.25,.5,1.,2.):
                    result=solve(r,kind,gap,N)
                    result["scale_eV"]=r["scale_eV"]
                    rows.append(result)
    doc=dict(run="G01-Q",producer_sha256=sha(Path(__file__)),g01n_science_sha256=sha(n),
        g01p_science_sha256=sha(previous/"science.json"),
        g01p_verification_sha256=sha(previous/"verification.json"),rows=rows,
        direct_bright_s=1,ground_density_kg_m3=2000,ground_relative_permittivity=4,
        shell_radius_m=2,drive="G01-N dipolar free surface charge held fixed",
        earth_comparison="planar static induced field stress; homogeneous ground and perfect bright conductor end cases",
        payload="absent",whole_craft_lift="uncertified",physical_survivors=0,full_regression="NOT_RUN")
    with (out/"science.json").open("x") as f: json.dump(doc,f,sort_keys=True,indent=2,allow_nan=False)
    for r in rows:
        if r["order"]==40 and r["kind"]!="vacuum":
            print(r["scale_eV"],r["kind"],r["gap_m"],r["craft_field_force_up_N"],r["fraction_shell_weight"])
    print("SCIENCE_SHA256",sha(out/"science.json"))
if __name__=="__main__": main(*map(Path,sys.argv[1:4]))
