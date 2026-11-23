"""Independent high-precision action derivatives, field matching and slip work."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys, time
import mpmath as m
m.mp.dps=45
out=Path(__file__).resolve().parent
run=out.parent
def sha(b):
    return hashlib.sha256(b).hexdigest()
def check(name, value):
    v["checks"][name]=bool(value)
    if not value:
        raise ValueError(name)
def demag(s):
    y=-m.expm1(-3*s)
    return (1-y)*m.hyp2f1(1,m.mpf("1.5"),m.mpf("2.5"),y)/3
def action(z,eta,a):
    E,B,q,u,s=z
    V=m.exp(u)
    O=m.exp(-eta*E*B)
    nu=1/(V*O**3)
    N=demag(s)
    strain=(2*m.exp(-s)+m.exp(2*s)-3)/2
    # Independent total over reference volume. Fixed particle number is one.
    rest=1+a*q*q/2+q**4/2+strain/8
    return (V*(E*E/N-B*B/(1-N))/2 - O*rest
            -V*O**4*(nu-1)**2/4 + q*E/O)

start,cpu=time.perf_counter(),time.process_time()
v=dict(utc=datetime.now(timezone.utc).isoformat(),verifier_sha256=sha(Path(__file__).read_bytes()),
       checks={}, action_gradient={}, next="NO_AUTOMATIC_PROMOTION")
try:
    raw=(run/"science.json").read_bytes()
    d=json.loads(raw)
    v["science_sha256"]=sha(raw)
    check("receipt", (run/"science.json.sha256").read_text().split()==[sha(raw),"science.json"]
          and sha((run/"source.py").read_bytes())==d["producer_sha256"]
          and d["status"]=="AFFINE_FAILS_LINEAR_QUADRUPOLE_BALANCE_DERIVED")
    for p,h in d["parents"].items():
        check("parent_"+Path(p).name,sha(Path(p).read_bytes())==h)
    for name,row in d["cases"].items():
        z=list(map(m.mpf,row["state"]))
        eta,a=m.mpf(row["eta"]),m.mpf(row["a"])
        err=max(abs(m.diff(lambda t:action(z[:i]+[t]+z[i+1:],eta,a),z[i])) for i in range(5))
        v["action_gradient"][name]=float(err)
        check(name+"_variation",err<m.mpf("1e-12"))
        E,B,q,u,s=z
        N=demag(s)
        theta=m.mpf(row["theta"])
        P=m.exp(-u+eta*E*B)*q
        # Recover uniform fields by separate linear matching with the local coefficients.
        eb=m.lu_solve(m.matrix([[1/N,theta],[-theta,1/(1-N)]]),m.matrix([-P,0]))
        check(name+"_interface",max(abs(eb[0]-E),abs(eb[1]-B))<m.mpf("1e-12"))
    g=d["cases"]["ordered"]
    r=d["cases"]["reversed"]
    check("external_mirror_and_reversal",g["exterior_B_over_E"]<0<r["exterior_B_over_E"] and
          abs(g["state"][1]+r["state"][1])<1e-12 and abs(g["theta"]+r["theta"])<1e-12)
    check("portal_off",abs(d["cases"]["portal_off"]["state"][1])<1e-12)
    check("unordered_off",max(map(abs,d["cases"]["unordered"]["state"]))<1e-12)
    check("sphere_shape_derivative",abs(m.diff(demag,0)+m.mpf(2)/5)<1e-35)
    # Unit-ball coordinates (r,t=cos polar angle). Integrate elastic virtual work
    # for the tangential, divergence-free test. The gradient has zero trace.
    E,B,q,u,s=map(m.mpf,g["state"])
    mu=m.mpf(1)/8
    factor=m.exp(-u-m.mpf(g["eta"])*E*B)*mu
    def density(rad,t):
        rr=rad**2*(1-t*t)
        zz=rad**2*t*t
        dr=-1+3*rr+3*zz
        hoop=-1+rr+3*zz
        dz=2-4*rr-6*zz
        return m.exp(-s)*(dr+hoop)+m.exp(2*s)*dz
    work=factor*3/2*m.quad(lambda rad:rad**2*m.quad(lambda t:density(rad,t),[-1,1]),[0,1])
    for t in (m.mpf("0.23"),m.mpf("0.73")):
        rr,zz=1-t*t,t*t
        normal=rr*(-1+rr+3*zz)+2*zz*(1-2*rr-zz)
        check("tangency_"+str(t),abs(normal)<1e-40)
    check("slip_work",abs(work-g["slip_work_per_volume"])<1e-12 and work< -1e-7)
    v["independent_slip_work_per_volume"]=float(work)

    # Differentiate the displacement itself, then form stress and its divergence.
    # Axisymmetric quadrupole Q=diag(-1/2,-1/2,1). No imposed boundary displacement.
    lin=d["linear_free_boundary"]
    A,Bc,C=map(m.mpf,lin["coefficients"])
    Q=[-m.mpf("0.5"),-m.mpf("0.5"),m.mpf(1)]
    def change(x,j,t):
        return x[:j]+[t]+x[j+1:]
    def disp(x,i):
        r2=sum(t*t for t in x)
        phi=sum(w*t*t for w,t in zip(Q,x))
        return (A+Bc*r2)*Q[i]*x[i]+C*phi*x[i]
    def stress(x,i,j):
        def grad(i,j):
            return m.diff(lambda t:disp(change(x,j,t),i),x[j])
        tr=sum(grad(k,k) for k in range(3)) if i==j else 0
        return (m.mpf(1)/2-2*mu/3)*tr+mu*(grad(i,j)+grad(j,i))
    x=list(map(m.mpf,["0.23","-0.31","0.54"]))
    body=max(abs(sum(m.diff(lambda t:stress(change(x,j,t),i,j),x[j])
                     for j in range(3))) for i in range(3))
    maxerr=0
    for t in [m.mpf(i)/8 for i in range(-8,9)]:
        x=[m.sqrt(1-t*t),m.mpf(0),t]
        ev=lin["normal_load_per_q2"]*(3*t*t-1)/2
        maxerr=max(maxerr,max(abs(sum(stress(x,i,j)*x[j] for j in range(3))-ev*x[i])
                              for i in range(3)))
    # Independent field energy slope with frozen unit polarization and theta0=1/4.
    def self_energy(ss):
        nn=demag(ss)
        return nn/(2*(1+nn*(1-nn)/16))
    from_work=-m.mpf(5)/3*m.diff(self_energy,0)
    check("quadrupole_drive",abs(from_work-lin["normal_load_per_q2"])<1e-13)
    check("bulk_and_free_traction",body<1e-12 and maxerr<1e-12)
    v["linear_residuals"]=dict(bulk=float(body),surface=float(maxerr))
    v["status"]="PASS_SCOPED_SOURCE_AND_LINEAR_FREE_BOUNDARY"
except Exception as exc:
    v.update(status="HOLD",error=str(exc))
v.update(wall_s=time.perf_counter()-start,cpu_s=time.process_time()-cpu)
raw=(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
with (out/"verification.json").open("xb") as f:
    f.write(raw)
with (out/"verification.json.sha256").open("x") as f:
    f.write(f"{sha(raw)}  verification.json\n")
print(v["status"],sha(raw),v.get("independent_slip_work_per_volume"),v.get("error",""))
sys.exit(v["status"]=="HOLD")
