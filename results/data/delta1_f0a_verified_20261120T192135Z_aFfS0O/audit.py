"""DELTA1-F0A. Free, open-circuit polar sphere in an isolated Maxwell X sector."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math, sys, time

out = Path(__file__).resolve().parent
data = Path("results/data")
f0 = "delta1_f0_20261120T190601Z_EHxGDA/"
locks = {
    f0+"science.json": "2feab292375dd33f7d97b66e71ad379ce9dd689dd4767052e06d68ede9850bb4",
    f0+"verify_34S2RK/verification.json": "b750a86cf37b255f15cacecec33ad5208773694991d5b39cb81c8a182584c052",
    "032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json":
        "9474b6782104abb5bd8dd5e893137621b30ad96109e3e52c5a01268794810b11",
    "032h17a12d1r3x3b7_finite_charge_shell_summary.json":
        "e08703d4b6cd256e007b2e4f46b861f803bca493e30de8e9196d878ff0749e19",
}
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def save(name, content):
    raw = (json.dumps(content, sort_keys=True, indent=2, allow_nan=False)+"\n").encode()
    with (out/name).open("xb") as f:
        f.write(raw)
    with (out/(name+".sha256")).open("x") as f:
        f.write(f"{digest(raw)}  {name}\n")
    return digest(raw)

start, cpu = time.perf_counter(), time.process_time()
record = {"run": "DELTA1-F0A", "utc": datetime.now(timezone.utc).isoformat(),
          "parents": locks, "producer_sha256": digest(Path(__file__).read_bytes()),
          "new_PDE_solves": 0, "full_regression": "PENDING", "F1": "HOLD"}
try:
    docs = {}
    for path, expected in locks.items():
        raw = (data/path).read_bytes()
        if digest(raw) != expected:
            raise ValueError("Parent SHA mismatch: "+path)
        docs[path] = json.loads(raw)
    mirror, = [v for v in docs.values() if "grid_results" in v]
    grid = mirror["grid_results"]["0.05"]
    modes = grid["multipole_modes"]
    e1, = [m["electric_exterior_energy_j"] for m in modes if m["ell"] == 1]
    radius = grid["global_energy"]["electric_source_support_radius_m"]

    # x^3 j1'(x). Bracket the first positive root, excluding the origin.
    def boundary(x):
        return (x*x-2)*math.sin(x)+2*x*math.cos(x)
    lo, hi = 2.0, 2.2
    if not (boundary(lo) > 0 > boundary(hi)):
        raise ArithmeticError("Missing root bracket")
    for _ in range(50):
        mid = (lo+hi)/2
        if boundary(mid) > 0:
            lo = mid
        else:
            hi = mid
    x = (lo+hi)/2
    record.update(status="CONDITIONAL_STATIC_SOURCE_CRITERION",
        model="Fixed 3D ball; isotropic quartic polarization; vacuum X; natural gradient boundary",
        action_density="I*Pdot^2/2 - a*P^2/2 - b*(P^2)^2/4 - k*|grad P|^2/2 + P.E_X",
        assumptions="I,b,k,epsilon_X positive; no free charge, drive, surface anchoring or screening",
        current="rho=-div(1_ball P); J=dt(1_ball P) for a fixed material region",
        ordered_branch="P0^2=-(a+1/(3*epsilon_X))/b > 0",
        first_root=x, lambda_unit_ball=x*x, critical_epsilon_k_over_R2=1/(3*x*x),
        source_radius_m=radius, critical_sqrt_epsilon_k_m=radius/(math.sqrt(3)*x),
        historical_preload_electric_dipole_energy_fraction=e1/sum(m["electric_exterior_energy_j"] for m in modes),
        scope="Static polarization Hessian after electrostatic elimination; two uniform rotation zero modes",
        missing=["microscopic X-charged material and coefficients","mechanics of source boundary",
                 "Y source","loaded 1 kg torus and Earth/craft response","complete operating energy"],
        qualified_gravity_bridges=0)
except Exception as exc:
    record.update(status="HOLD", error=str(exc))
record.update(wall_s=time.perf_counter()-start, cpu_s=time.process_time()-cpu)
print(record["status"], save("science.json", record), out, flush=True)
sys.exit(record["status"] == "HOLD")
