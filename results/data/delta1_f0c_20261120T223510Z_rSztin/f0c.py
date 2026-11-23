"""F0C. Frozen off-state trace, quadratic axial response, and a silent source mode."""
import hashlib, json, math, os, sys, time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.sparse import bmat, coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.optimize import brentq
from scipy.special import spherical_jn

out = Path(__file__).resolve().parent
data = Path("results/data")
b = data/"delta1_f0b_20261120T193444Z_Gmr1NE"
pins = {
    b/"science.json": "fd21173471942c8e21b2659d25ac8a8b3790ede8f0dce45717d4e38f7206963c",
    b/"verify_ZuiGh3/verification.json": "9752ac820bd93247477a2c3f282e0eed095dc4182f3ac5c7975feb8acb22e24b",
    data/"delta1_f0_20261120T190601Z_EHxGDA/science.json": "2feab292375dd33f7d97b66e71ad379ce9dd689dd4767052e06d68ede9850bb4",
    data/"032h17a12d1r3x3b0_inverse_loading_summary.json": "0b37ba0acbf31da4aaa546fad5edbca448474fcf8a94f058d09bf0836161884a",
    Path("src/antigravity_research/agminer/hook17_concurrent_u1_fieldstrength_metric.py"): "2fb2094de5995aab5172fc825bd30d895ffbb163d1a3418105c808c19fa50b99",
    Path("src/antigravity_research/agminer/hook17_f2_strong_payload_loading_rescue.py"): "e1296794c25a4d0e4d5634c7e7d543a0b488b8d2a1963afcf7878bea1c1b99e7",
}
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def put(name, obj):
    raw = (json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+"\n").encode()
    with (out/name).open("xb") as f:
        f.write(raw)
    h = hashlib.sha256(raw).hexdigest()
    with (out/(name+".sha256")).open("x") as f:
        f.write(f"{h}  {name}\n")
    return h

def require(ok, why):
    if not ok:
        raise ValueError(why)

def solve(h, L, flip, case):
    # Open exterior approximated by a box. E=-grad(phi), B=(-psi_z,psi_r)/r.
    n = round(L/h)
    require(abs(n*h-L)<1e-12, "mesh extent")
    ids = np.arange((2*n+1)*(n+1)).reshape(2*n+1,n+1)
    rr, zz = np.meshgrid(np.arange(n+1)*h,(np.arange(2*n+1)-n)*h)
    a, b0, c, d = (v.ravel() for v in
                    (ids[:-1,:-1],ids[:-1,1:],ids[1:,:-1],ids[1:,1:]))
    triangles = [(a,b0,d),(a,d,c)] if not flip else [(a,b0,c),(b0,d,c)]
    tri = np.vstack([np.column_stack(t) for t in triangles])
    r, z = rr.ravel()[tri], zz.ravel()[tri]
    rc, zc = r.mean(axis=1), z.mean(axis=1)
    def grad(coords, sign):
        vals = sign*(np.roll(coords,-1,axis=1)-np.roll(coords,-2,axis=1))/h**2
        return coo_matrix((vals.ravel(),(np.repeat(np.arange(len(tri)),3),tri.ravel())),
                          shape=(len(tri),ids.size)).tocsr()
    gr, gz = grad(z,1), grad(r,-1)
    free = (rr<L-h/2) & (abs(zz)<L-h/2)
    flux_free = free & (rr>0)
    er, ez = -gr[:,free.ravel()], -gz[:,free.ravel()]
    br = (-gz[:,flux_free.ravel()]).multiply((1/rc)[:,None]).tocsr()
    bz = gr[:,flux_free.ravel()].multiply((1/rc)[:,None]).tocsr()
    w = math.pi*rc*h*h
    ball = np.hypot(rc,zc)<model.SOURCE_RADIUS_M
    density = model.payload_density_profile_kg_m3(rc,zc)
    beta = model.loading_coefficient_z(density,model.REFERENCE_PORTAL_SCALE_EV)-1
    eta = 0.0 if case=="off" else 0.25
    # In the F0B convention -rho*exp(-eta E.B) gives +eta*rho*E.B.
    theta = eta*ball + (beta if case=="loaded" else 0.)
    def prod(A,weights,B):
        return A.T @ B.multiply(weights[:,None])
    K = prod(er,w,er)+prod(ez,w,ez)
    M = prod(br,w,br)+prod(bz,w,bz)
    C = prod(er,w*theta,br)+prod(ez,w*theta,bz)
    op = bmat([[K,C],[-C.T,M]],format="csc")
    rhs = np.r_[-ez.T@(w*ball), np.zeros(M.shape[0])]
    x = spsolve(op,rhs)
    residual = float(np.linalg.norm(op@x-rhs)/np.linalg.norm(rhs))
    require(residual<1e-7,"field residual")
    p, s = np.split(x,[K.shape[0]])
    E1,E2,B1,B2 = er@p,ez@p,br@s,bz@s
    # Reconstruct metric first, then differentiate along +z.
    logO = -eta*(E1*B1+E2*B2)
    S = logO.reshape(2,2*n,n).mean(axis=0)
    A = -np.gradient(S,h,axis=0)
    R, Z = rr[:-1,:-1]+h/2, zz[:-1,:-1]+h/2
    mask = model.payload_density_profile_kg_m3(R,Z)>0
    cell = np.unravel_index(np.argmin(np.where(mask,A,np.inf)),A.shape)
    # Entire chord lies inside the torus. Its mean signed response avoids
    # differentiating a single cell; negative implies an inward point in that interpolant.
    z0 = model.payload_center_z_m()
    chord = [(z0-0.10,1.),(z0+0.10,1.)]
    val = RegularGridInterpolator((Z[:,0],R[0]),S)(chord)
    work = -float(np.dot(w*ball,E2)/np.sum(w*ball))
    # A zero-mean axial variation kills the uniform local material force.
    # Its gradient costs no first variation at uniform P. Nonzero work tests
    # the part of the polarization Euler equation lost by the uniform ansatz.
    Wb=w*ball
    mean_z=float(Wb@zc/Wb.sum())
    quadrupole=float(Wb@(-0.5*rc*E1+(zc-mean_z)*E2)/(model.SOURCE_RADIUS_M*Wb.sum()))
    result = dict(source_quadrupole_work=quadrupole,h=h,L=L,flip=flip,case=case,residual=residual,
        mass_kg=float(w@density),peak_beta=float(beta.max()),
        curvature=-0.35+work,minimum=float(A[cell]),maximum=float(A[mask].max()),
        worst_r_z_m=[float(R[cell]),float(Z[cell])],sample_count=int(mask.sum()),
        chord_mean=float((val[0]-val[1])/0.2))
    if case=="loaded" and flip:
        P,Sflux = np.zeros_like(rr),np.zeros_like(rr)
        P[free],Sflux[flux_free] = p,s
        with (out/"potentials.npz").open("xb") as f:
            np.savez_compressed(f,phi=P,psi=Sflux)
        result["potentials_sha256"] = digest(out/"potentials.npz")
    return result

wall,cpu=time.perf_counter(),time.process_time()
record=dict(utc=datetime.now(timezone.utc).isoformat(),producer=digest(Path(__file__)),
    parents={},rows=[],next="NO_AUTOMATIC_PROMOTION",full_regression="PENDING",
    action="L2=(E^2-B^2)/2+theta E.B+P.E-a P^2/2-k |grad P|^2/2",
    assumptions="F0B dust trace sign; archived 1-keV load magnitude; R=2 m; canonical unit axial polarization trial; natural polarization boundary; unstrained off state",
    units="minimum, maximum and chord_mean are a_z/(c^2 q^2), inverse metres, q in F0B units",
    energy="ENERGY_UNDETERMINED",earth_craft="NOT_DERIVED")
try:
    for path,expected in pins.items():
        require(digest(path)==expected,"parent SHA "+str(path))
    source=json.loads((b/"science.json").read_bytes())
    for rel,expected in source["parents"].items():
        path=Path(rel)
        require(digest(path)==expected,"ancestor SHA "+rel)
        pins[path]=expected
    record["parents"]={str(p):v for p,v in pins.items()}
    sys.path.insert(0,str(Path("src").resolve()))
    from antigravity_research.agminer import hook17_f2_strong_payload_loading_rescue as model
    require(abs(model.geometric_standoff_m()-1)<1e-12 and model.PAYLOAD_MASS_KG==1,
            "geometry")
    require(source["cases"]["ordered"]["a"]==-0.35 and source["parameters"]["mass"]==1
            and source["cases"]["ordered"]["eta"]==0.25,"F0B parameters")
    x1=brentq(lambda x:spherical_jn(1,x,derivative=True),2,2.2)
    record.update(isolated_curvature=-0.35+1/(3+2*0.25**2/3),
        loaded_uniform_curvature_upper=-0.35+1/3,
        silent_k_over_R2_threshold=0.35/x1**2,
        silent_mode="P=j1(x1*r/R)*(ez cross rhat); tangent, div P=0; E=B=0 for any torus trace",
        physical_minimum=None,reason="k/R^2 unspecified; axial trial is not a selected loaded source eigenmode")
    for args in [(0.075,6,False,"off"),(0.075,6,False,"vacuum"),
                 (0.075,6,False,"loaded"),(0.05,6,False,"loaded"),
                 (0.05,7.5,False,"loaded"),(0.05,7.5,True,"loaded")]:
        row=solve(*args)
        record["rows"].append(row)
        print(row["case"],row["h"],row["L"],row["flip"],"min",row["minimum"],
              "chord",row["chord_mean"],flush=True)
    rows=record["rows"][2:]
    record["trial_diagnostics"]=dict(
        minimum_changes_mesh_box_diagonal=[abs(y["minimum"]-x["minimum"]) for x,y in zip(rows,rows[1:])],
        both_chord_signs=min(r["chord_mean"] for r in rows)<0<max(r["chord_mean"] for r in rows),
        all_sampled_minima_inward=all(r["minimum"]<0 for r in rows),
        uncertainty="observed variation only; no continuum enclosure",
        continuum_outcome="NUMERICAL_INCONCLUSIVE")
    record["status"]="LOADED_AXIAL_TRIAL_COMPLETE_PHYSICAL_MODE_UNDERDETERMINED"
except Exception as exc:
    record.update(status="HOLD",error=repr(exc))
record.update(wall_s=time.perf_counter()-wall,cpu_s=time.process_time()-cpu)
print(record["status"],put("science.json",record),record.get("error",""))
sys.exit(record["status"]=="HOLD")
