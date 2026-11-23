"""DELTA1-F0B: open X/Y fields and a free, uniform polar solid. Canonical units."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys, time
import numpy as np
from scipy.optimize import root

out = Path(__file__).resolve().parent
data = Path("results/data")
base = data/"delta1_f0a_verified_20261120T192135Z_aFfS0O"
pins = {
    base/"replay_lhVLr2/science.json": "baa5ec84bae337af4927d79b2ebd9380b0aaccf01fa28947aa4f8530c9b6ee44",
    base/"replay_lhVLr2/verify/verification.json": "71c4b122351c939d32faa8c1fe02fa7483cc92759a5ff03b7e87fe8885d0234c",
    base/"interface_replay_XFyASR/interface.json": "7a7ce0b430fa8c2828320a2751153ec575102d8a7da46848b5ff00e911c944cc",
    data/"032h17a12d1r3x1_lorentzian_sign_audit_summary.json": "8c3a7de0fea08ebdc649992cb12e8942bf1ba7b72607f5c06cd56ae388caede5",
    data/"032h17a12d1r3x3b8_spherical_interface_screening_summary.json": "57f73dad0ffdefd4e44eaa00ca6906403dead256bc17683b2cb8a0533e855b95",
}
def sha(b):
    return hashlib.sha256(b).hexdigest()
def save(path, obj):
    raw=(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
    with path.open("xb") as f:
        f.write(raw)
    with Path(str(path)+".sha256").open("x") as f:
        f.write(f"{sha(raw)}  {path.name}\n")
    return sha(raw)

# N=(1/2) integral_0^infty dt/[(t+exp(-s))(t+exp(2s))^(3/2)].
# t=v^(-2)-1 gives a smooth finite-interval integrand, including at s=0.
x, weights = np.polynomial.legendre.leggauss(32)
v=(1+x)/2
def depol(s):
    A=1+np.expm1(-s)*v*v
    C=1+np.expm1(2*s)*v*v
    term=(weights/2)*v*v/(A*C**1.5)
    deriv=v*v*(np.exp(-s)/A-3*np.exp(2*s)/C)
    return np.sum(term),np.sum(term*deriv)

K, mu, b4, mass = 0.5, 0.125, 2.0, 1.0
def evaluate(y, eta, a):
    E,B,q,u,s=y
    N,Ns=depol(s)
    n=np.exp(-u)
    O=np.exp(-eta*E*B)
    nu=n/O**3
    h=(2*np.exp(-s)+np.exp(2*s)-3)/2
    w=mass+a*q*q/2+b4*q**4/4+mu*h
    W=nu*w+K*(nu-1)**2/2
    pressure=K*(nu*nu-1)/2
    P=n*q/O
    theta=-eta*(O**4*(3*pressure-W)-P*E)
    field=E*E/(2*N)-B*B/(2*(1-N))
    shear=O*n*mu*(np.exp(2*s)-np.exp(-s))
    res=[E/N+P+theta*B, -B/(1-N)+theta*E,
         -O**4*nu*(a*q+b4*q**3)+n*E/O,
         field+O**4*pressure,
         -Ns*(E*E/N**2+B*B/(1-N)**2)/2-shear]
    return np.array(res), dict(state=y.tolist(),N=float(N),theta=float(theta),
        exterior_B_over_E=(float(-N*theta) if E!=0 else None), pressure=float(pressure),
        shear_difference=float(shear), slip_work_per_volume=float(-0.8*shear))

wall,cpu=time.perf_counter(),time.process_time()
report=dict(branch="DELTA1-F0B",utc=datetime.now(timezone.utc).isoformat(),
    producer_sha256=sha(Path(__file__).read_bytes()),parents={str(k):h for k,h in pins.items()},
    parameters=dict(K=K,mu=mu,b4=b4,mass=mass), cases={}, full_regression="PENDING",
    action="V*(E^2/(2*N)-B^2/(2*(1-N))-Omega^4*W+n*q*E/Omega)",
    assumptions="Free homogeneous spheroid, insulating, unanchored director, no free sheets or surface action; dimensionless",
    missing="Nonuniform material equilibrium, loaded torus, gravity, SI cost and microscopic X coupling",
    new_PDE_solves=0,next="NO_AUTOMATIC_PROMOTION")
try:
    for p,h in pins.items():
        if sha(p.read_bytes())!=h:
            raise ValueError("Parent SHA mismatch: "+str(p))
    for name,eta,a,seed in [
        ("ordered",0.25,-0.35,[-0.04,-0.006,0.12,0.003,0.006]),
        ("reversed",-0.25,-0.35,[-0.04,0.006,0.12,0.003,0.006]),
        ("portal_off",0.,-0.35,[-0.035,0.,0.1,0.003,0.005]),
        ("unordered",0.25,0.35,[0.,0.,0.,0.,0.])]:
        solve=root(lambda y:evaluate(y,eta,a)[0],seed,tol=1e-11)
        res,row=evaluate(solve.x,eta,a)
        err=float(np.max(np.abs(res)))
        row.update(eta=eta,a=a,affine_residual=err,solver_success=bool(solve.success))
        report["cases"][name]=row
        if not solve.success or not np.isfinite(err) or err>1e-9:
            raise ValueError("AFFINE_SOLVE_HOLD: "+name)
        if name!="unordered" and abs(solve.x[2])<0.01:
            raise ValueError("Ordered seed reached the trivial sector")
    if abs(report["cases"]["ordered"]["slip_work_per_volume"])<1e-7:
        raise ValueError("Slip work numerically inconclusive")

    # Leading quadrupole sector at fixed small q. Units R=1, coefficients per q^2.
    # eta*m is the off-state trace coefficient; t2 comes from virtual shape work.
    t0=report["cases"]["ordered"]["eta"]*mass
    t2=(1+t0**2/9)/(3*(1+2*t0**2/9)**2)
    lame=K-2*mu/3
    matrix=[[0,14*mu+4*lame,14*mu+10*lame],
            [1,2,1],[0,2*mu+2*lame,4*mu+5*lame]]
    coeff=np.linalg.solve(matrix,[0,0,t2])
    report["linear_free_boundary"]=dict(
        coefficients=coeff.tolist(), normal_load_per_q2=t2,
        surface_displacement_per_q2=float(sum(coeff)), normalized_radius=1,
        scope="l=2 static mechanical response at fixed small polarization, no external clamp")
    report["status"]="AFFINE_FAILS_LINEAR_QUADRUPOLE_BALANCE_DERIVED"
except Exception as exc:
    report.update(status="HOLD",error=str(exc))
report.update(wall_s=time.perf_counter()-wall,cpu_s=time.process_time()-cpu)
print(report["status"],save(out/"science.json",report),out)
if "error" in report:
    print(report["error"])
sys.exit(report["status"]=="HOLD")
