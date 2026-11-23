"""Independent polynomial Rayleigh-Ritz and electrostatic controls for DELTA1-F0A."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math, sys, time
import numpy as np
from scipy.linalg import eigh

out = Path(__file__).resolve().parent
run = out.parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()
start, cpu = time.perf_counter(), time.process_time()
v = {"utc": datetime.now(timezone.utc).isoformat(), "checks": {}, "ritz": [],
     "verifier_sha256": sha(Path(__file__).read_bytes())}
def check(name, value):
    v["checks"][name] = bool(value)
    if not value:
        raise ValueError(name)

try:
    raw = (run/"science.json").read_bytes()
    s = json.loads(raw)
    v["science_sha256"] = sha(raw)
    check("science_and_code", (run/"science.json.sha256").read_text().split() ==
          [sha(raw), "science.json"] and sha((run/"audit.py").read_bytes()) == s["producer_sha256"]
          and s["status"] == "CONDITIONAL_STATIC_SOURCE_CRITERION")
    for path, h in s["parents"].items():
        check("parent_"+path, sha((Path("results/data")/path).read_bytes()) == h)
    # Independent l=1 weak form: integral(r^2*f'*g' + 2*f*g) / integral(r^2*f*g).
    for n in (1, 2, 3, 4):
        powers = np.arange(1, 2*n, 2)
        i, j = powers[:, None], powers[None, :]
        K = (i*j+2)/(i+j+1)
        M = 1/(i+j+3)
        v["ritz"].append(float(eigh(K, M, eigvals_only=True)[0]))
    ev = v["ritz"][-1]
    check("variational_convergence", all(a>b for a,b in zip(v["ritz"],v["ritz"][1:]))
          and abs(v["ritz"][0]-5)<1e-12 and abs(ev-s["lambda_unit_ball"])<1e-7)
    check("threshold", abs(1/(3*ev)-s["critical_epsilon_k_over_R2"])<2e-9)
    check("curl_signs", 0.05*ev-1/3 < 0 < 0.10*ev-1/3)

    # Normalize R=P=epsilon=1. phi_in=A*r*cos(theta), phi_out=B*cos(theta)/r^2.
    # Continuity of potential and of normal D: A-B=0, A+2B=1.
    A, B = np.linalg.solve([[1.,-1.],[1.,2.]],[0.,1.])
    inside, outside = 2*math.pi*A*A/3, 4*math.pi*B*B/3
    check("depolarization_and_energy", abs(A-1/3)<1e-14 and
          abs((inside+outside)/(4*math.pi/3)-1/6)<1e-14)
    # Independent nonlinear radial curvature, a=-1, b=epsilon=1.
    p = math.sqrt(2/3)
    def energy(q):
        return -q*q/2 + q**4/4 + q*q/6
    h = 1e-4
    check("ordered_radial_curvature", abs((energy(p+h)-2*energy(p)+energy(p-h))/h**2-4/3)<1e-6)
    check("disordered_control", 0.2+1/3 > 0 and energy(p)<energy(0))
    grid = json.loads((Path("results/data")/
        "032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json").read_bytes())["grid_results"]["0.05"]
    dip, = [m for m in grid["multipole_modes"] if m["ell"]==1]
    frac = dip["electric_exterior_energy_j"]/grid["global_energy"]["new_electric_exterior_energy_j"]
    check("archived_dipole_normalization", abs(frac-s["historical_preload_electric_dipole_energy_fraction"])<1e-12)
    v["status"] = "PASS_SCOPED_SOURCE_ALGEBRA"
except Exception as exc:
    v.update(status="HOLD", error=str(exc))
v.update(wall_s=time.perf_counter()-start, cpu_s=time.process_time()-cpu)
raw = (json.dumps(v, sort_keys=True, indent=2, allow_nan=False)+"\n").encode()
with (out/"verification.json").open("xb") as f:
    f.write(raw)
with (out/"verification.json.sha256").open("x") as f:
    f.write(f"{sha(raw)}  verification.json\n")
print(v["status"], sha(raw), v["ritz"], v.get("error",""), flush=True)
sys.exit(v["status"] == "HOLD")
