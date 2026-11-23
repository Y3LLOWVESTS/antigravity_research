"""Independent G01-O checker. Algebraic proof plus high-precision boundary matching."""
import hashlib
import json
import sys
from pathlib import Path
import mpmath as m
import sympy as sy

root, out = map(Path,sys.argv[1:3])
m.mp.dps=75
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def require(ok, reason):
    if not ok:
        raise ValueError(reason)
def equal(x,y,tol=1e-12):
    require(abs(x-y)<=tol*max(abs(y),1),"independent calculation drift")
def identity(expr):
    require(sy.factor(expr)==0,"symbolic identity failed")

# In the shell use potentials of E_spectator,E_X,H_Y. Both growing r and
# decaying r^-2 solutions are necessary. The common radius is normalized
# to 1. The core has only growing and exterior only decaying modes.
# In this symbolic basis scale each potential by its charge projection,
# so the driving vector is (1,1,0) for 0<s<1. Endpoints are separate limits.
f,s,k,z=sy.symbols("f s k z")
I=sy.eye(3)
M=sy.Matrix([[1+k*(1-s),k*s,0],[k*(1-s),1+k*s+z**2,z],[0,z,1]])
D=9*M+2*f*(M-I)**2
N=D.adjugate()*2*((3-f)*M+f*I)*sy.Matrix([1,1,0])
P=sy.Poly(sy.expand(N[1]+N[2]),f)
identity(9*N[0]-(9+2*f*z**2)*N[1])
identity(P.eval(0)-486*(k+1))
identity(P.eval(3/z)-54*k*(z-3)*(2*z*(1-s)+3)/z)
identity(P.nth(2)+12*z**2*((2*z+3)*k*(1-s)+3*z))
# Hence P is concave and positive on [0,3/z), for z>3,k>=0,s in [0,1].
# D is nonsingular: in a canonical basis its eigenvalues are
# 9*lambda+2*f*(lambda-1)^2 with lambda>0.

def medium(sval,eps,theta):
    n=m.matrix([m.sqrt(1-sval),m.sqrt(sval),0])
    M=m.eye(3)+(eps-1)*n*n.T
    M[1,1]+=theta**2
    M[1,2]=M[2,1]=theta
    return M,n
def bead(sval,eps,theta):
    matrix,n=medium(sval,eps,theta)
    # Applied potential -n*r plus scattered w/r^2. Both components
    # of potential and normal flux match. Response is n.w.
    w=m.lu_solve(matrix+2*m.eye(3),(matrix-m.eye(3))*n)
    return m.fdot(w,n)
def direct_shell(sval,eps,theta,fraction):
    mat,n=medium(sval,eps,theta)
    a=(1-fraction)**(m.mpf(1)/3)
    def conditions(q):
        core,grow,decay,outer=[q[i:i+3,:] for i in (0,3,6,9)]
        return m.matrix(list(core-grow-decay/a**3)
            +list(core-mat*(grow-2*decay/a**3))
            +list(outer-grow-decay)
            +list(2*outer+mat*(grow-2*decay)))
    A=m.matrix(12)
    for j in range(12):
        A[:,j]=conditions(m.eye(12)[:,j])
    rhs=m.matrix(12,1)
    rhs[9:12,:]=n
    return 2*m.lu_solve(A,rhs)[9:12,:]

science=json.loads((out/"science.json").read_bytes())
require(sha(out/"produce.py")==science["producer_sha256"],"producer drift")
parent=root/"results/gravity2/g01n_shell_source_v1/science.json"
require(sha(parent)==science["parent_science_sha256"]==
        "7635896c65e47e64ffa772651a55605e38499790b44a7c37a582c537a8c752fb","science parent")
data=json.loads(parent.read_bytes())
require(science["laboratory"]["measured_alpha_over_alpha0"]==[[.21,.13],[0,.33],[.25,.14]],"paper table")
bead_min=(m.mpf("1.78")/m.mpf("2.50"))**3
limit=min(m.mpf(str(c))+3*m.mpf(str(e)) for c,e in science["laboratory"]["measured_alpha_over_alpha0"])
equal(limit,.60)
equal(bead(1,3,0),.4)
equal(bead(m.mpf(".37"),1,0),0)
equal(bead(0,3,17),.4)
equal(bead(m.mpf(".37"),3,11),bead(m.mpf(".37"),3,-11))
require(0.67<bead_min/0.4 and bead_min<limit,"radius-control failure")
require(len(science["rows"])==2,"row count")
checks=[]
for row,r in zip(science["rows"],[r for r in data["rows"] if r["eps_r"]==3.8]):
    equal(row["portal_scale_eV"],r["scale_eV"])
    t=m.mpf(r["theta"])
    u=m.mpf(r["exterior_electric_dipole_J"])
    lab=t*1000/2200
    # Solve for s with a boundary-matched polarizability.
    response=lambda x: bead(x,1,lab)*bead_min/m.mpf(".4")
    smax=m.findroot(lambda x: response(x)-limit,(m.mpf(".4"),m.mpf(".9")),solver="secant")
    equal(smax,row["lab_s_max"])
    # Test a fixed-charge shell at the bounding k=0 thickness from the proof.
    def energy_bound(x):
        fields=direct_shell(x,1,t,3/t)
        equal(fields[2]/fields[1],-1)
        return u*m.fdot(fields,fields)/fields[1]**2
    e=energy_bound(smax)
    equal(e,row["vacuum_exterior_J_at_lab_bound_lower"])
    equal(energy_bound(m.mpf(row["energy_s_strict_min"])),1e7,1e-8)
    equal(response(m.mpf(row["energy_s_strict_min"])),row["minimum_alpha_over_alpha0_at_energy_bound"])
    require(smax<row["energy_s_strict_min"] and e>1e7,"unexpected overlap")
    # Interior/exterior matching for an ordinary dielectric on either side
    # of the bounding thickness. Validate the spectator ratio independently.
    for thickness in (2/t,4/t):
        fields=direct_shell(smax,m.mpf("3.8"),t,thickness)
        equal(fields[0]/fields[1],m.sqrt((1-smax)/smax)*(1+2*thickness*t**2/9))
    checks.append(dict(scale_eV=float(r["scale_eV"]),lab_limit=float(smax),exterior_floor_J=float(e)))
verification=dict(status="PASS_SCOPED_IDENTITIES_AND_TWO_SCALE_NONOVERLAP",checks=checks,
    verified_by="exact polynomial certificates and independent 12-equation interface solve",
    verifier_sha256=sha(Path(__file__)),science_sha256=sha(out/"science.json"),full_regression="NOT_RUN")
with (out/"verification.json").open("x") as stream:
    json.dump(verification,stream,indent=2,sort_keys=True,allow_nan=False)
    stream.write("\n")
print(json.dumps(verification,indent=2))
print("VERIFICATION_SHA256",sha(out/"verification.json"))
