"""F0A transfer test. Evaluate the unsourced Y boundary residual on the X-only sphere."""
import hashlib, json, math, time
from datetime import datetime, timezone
from pathlib import Path

here = Path(__file__).resolve().parent
run = here.parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()
start, cpu = time.perf_counter(), time.process_time()
d = {"utc": datetime.now(timezone.utc).isoformat(), "producer_sha256": sha(Path(__file__).read_bytes()),
     "assumptions": "B_Y=0, no free Y sheet current, step theta, fixed sphere, continuous E_X tangent",
     "jump_convention": "outside minus inside; outward unit normal",
     "tests": {}, "new_PDE_solves": 0, "F1": "HOLD"}
def check(k, pred):
    d["tests"][k] = bool(pred)
    if not pred:
        raise ValueError(k)
try:
    pins = {
        run/"science.json": "9fd210b534a9eccedf4b2e81553fc957edb0cd9de7f79c6a4420c725ba3cf9f1",
        run/"verify_TniiUP/verification.json": "d8ab8970e2445bced8b9f07cd05c83f70c421d36c898105746f6f190a51d53e5",
        Path("src/antigravity_research/agminer/hook17_fdual_f_r3x1_lorentzian_sign_audit.py"):
            "6f1bf0922712a81e860075a71201af49c7870fa18fe2c21e7f576bb46da97531",
    }
    d["parents"] = {p.name:h for p,h in pins.items()}
    for p,h in pins.items():
        check("sha_"+p.name, sha(p.read_bytes())==h)

    # Normalize R=1 and P0/(3 epsilon_X)=1. H_Y=B_Y-theta E_X.
    # theta_inside=1, theta_outside=0. Purely electric field has E_theta=sin(theta).
    def jump(mu, theta_in=1., theta_out=0., amplitude=1.):
        return -(theta_out-theta_in)*amplitude*math.sqrt(max(0.,1-mu*mu))
    def integral(f):
        # Composite Simpson in mu=cos(theta); azimuth is integrated analytically.
        n=16
        vals=[f(-1+2*i/n) for i in range(n+1)]
        return (2/n)/3*(vals[0]+vals[-1]+4*sum(vals[1:-1:2])+2*sum(vals[2:-1:2]))
    rms=math.sqrt(integral(lambda u:jump(u)**2)/2)
    surface=2*math.pi*integral(lambda u:jump(u)*math.sqrt(max(0.,1-u*u)))
    volume=2*(4*math.pi/3)  # curl(z_hat cross r)=2*z_hat, H_Y inside=+z_hat.
    check("signed_weak_variation", abs(surface-volume)<1e-12 and abs(-surface-volume)>1)
    check("surface_rms", abs(rms-math.sqrt(2/3))<1e-12)
    check("pole_equator_and_reversed_step", jump(1)==0 and jump(0)==1 and jump(0,0,1)==-1)
    check("uniform_coefficient_or_source_off", jump(0,1,1)==0 and jump(0,1,0,0)==0)
    d.update(status="Y_ZERO_FAILS_AT_A_NONZERO_TRACE_COEFFICIENT_JUMP", normalized_rms=rms,
             boundary_weak_work=surface, volume_weak_work=volume, physical_jump_value="UNDETERMINED",
             stop="Actual trace/material action and reciprocal Y response required; no force inferred")
except Exception as exc:
    d.update(status="HOLD_ERROR", error=str(exc))
d.update(wall_s=time.perf_counter()-start,cpu_s=time.process_time()-cpu)
raw=(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
with (here/"interface.json").open("xb") as f:
    f.write(raw)
with (here/"interface.json.sha256").open("x") as f:
    f.write(f"{sha(raw)}  interface.json\n")
print(d["status"],sha(raw),here,flush=True)
raise SystemExit(d["status"]=="HOLD_ERROR")
