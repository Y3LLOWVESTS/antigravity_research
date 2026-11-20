"""Independent F0 receipt, archive, and local action checks. No solver imports."""
import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

out = Path(__file__).resolve().parent
run = out.parent
wall, cpu = time.perf_counter(), time.process_time()
checks = {}

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def check(name, condition):
    checks[name] = bool(condition)
    if not condition:
        raise ValueError(name)

record = {"utc": datetime.now(timezone.utc).isoformat(),
          "verifier_sha256": digest(Path(__file__).read_bytes())}
try:
    for name in ("parents.txt", "science.json", "receipt.json"):
        expected = f"{digest((run/name).read_bytes())}  {name}\n"
        check("sidecar_" + name, (run/(name+".sha256")).read_text() == expected)
    manifest = (run/"parents.txt").read_bytes()
    check("independent_manifest_lock", digest(manifest) ==
          "408e0f2eed8138097506fdee25508cf6cc4c375fe24fa8f79b615366e15161ed")
    for line in manifest.decode().splitlines():
        expected, path = line.split("  ", 1)
        check("parent_" + path, digest(Path(path).read_bytes()) == expected)
    science_bytes = (run/"science.json").read_bytes()
    record["science_sha256"] = digest(science_bytes)
    check("independent_science_lock", record["science_sha256"] ==
          "2feab292375dd33f7d97b66e71ad379ce9dd689dd4767052e06d68ede9850bb4")
    receipt = json.loads((run/"receipt.json").read_bytes())
    check("producer_and_receipt", receipt["status"] == "ARCHIVE_AUDIT_COMPLETE" and
          receipt["producer_sha256"] == digest((run/"audit.py").read_bytes()) and
          receipt["science_sha256"] == record["science_sha256"])
    record["receipt_sha256"] = digest((run/"receipt.json").read_bytes())

    # The original solver result is an additional witness. Record its actual hash.
    data = Path("results/data")
    name = "032h17a12d1r3x1_lorentzian_sign_audit_summary.json"
    original = (data/name).read_bytes()
    record["local_R3X1_summary_sha256"] = digest(original)
    x1 = json.loads(original)
    b0 = json.loads((data/"032h17a12d1r3x3b0_inverse_loading_summary.json").read_bytes())
    b4 = json.loads((data/"032h17a12d1r3x3b4_directional_com_summary.json").read_bytes())
    check("R3X1_certificate", x1["lorentzian_sign_and_direct_solver_pass"] and
          not x1["independent_microscopic_source_realized"])
    for h in (0.075, 0.050):
        grid, = [g for g in x1["grids"] if g["h_m"] == h]
        full, = [q for q in grid["rows"] if q["theta_sign"] == 1 and q["lambda"] == 1]
        off, = [q for q in grid["rows"] if q["theta_sign"] == 1 and q["lambda"] == 0]
        a, = [g for g in b0["grids"] if g["h_m"] == h]
        b, = [g["fully_loaded"] for g in b4["grids"] if g["h_m"] == h]
        check(f"native_sign_and_load_{h}", full["solve_success"] and
              math.isclose(off["minimum_payload_acceleration_m_s2"], 9.80665, abs_tol=1e-6) and
              math.isclose(full["minimum_payload_acceleration_m_s2"],
                           a["fully_loaded_min_a_m_s2"], rel_tol=0, abs_tol=1e-5) and
              math.isclose(full["minimum_payload_acceleration_m_s2"],
                           b["minimum_payload_acceleration_m_s2"], rel_tol=0, abs_tol=1e-5) and
              grid["sign_certificate"]["corrected_positive_K_coupling_signs"] == [1, -1])

    # Dimensionless derivative controls only. These numbers are not source parameters.
    def lam(p, t, coupling=1.0):
        sigma = coupling * (0.31*p - 0.12*p*p)
        return math.exp(4*sigma) * t * coupling * (0.31 - 0.24*p)

    p, t, dp, dt = 0.23, -0.8, 0.4, 0.6
    sp = 0.31 - 0.24*p
    fac = math.exp(4*(0.31*p - 0.12*p*p))
    exact = fac*(sp*dt + t*(4*sp*sp - 0.24)*dp)
    errors = []
    for h in (1e-3, 5e-4):
        fd = (lam(p+h*dp, t+h*dt) - lam(p-h*dp, t-h*dt))/(2*h)
        errors.append(abs(fd-exact))
    check("trace_second_variation", errors[1] < 1e-8 and errors[1] < 0.35*errors[0])
    record["trace_variation_fd_errors"] = errors
    check("trace_and_coupling_off", lam(p, 0) == 0 and lam(p, t, 0) == 0)

    grad_p = (0.4, -0.3)
    def wedge(a, b):
        return a[0]*b[1] - a[1]*b[0]

    for label, grad_t in (("interface", (0.2, 0.5)), ("uniform_trace", (0.0, 0.0))):
        h = 1e-5
        grad_lam = [(lam(p+h*u, t+h*v)-lam(p-h*u, t-h*v))/(2*h)
                    for u, v in zip(grad_p, grad_t)]
        check(label, abs(wedge(grad_lam, grad_p)-fac*sp*wedge(grad_t, grad_p)) < 1e-9)

    def lag(e, b):
        return 0.5*(e*e-b*b) + 0.7*e*b

    e, b, h = 0.4, -0.6, 0.01
    mixed = (lag(e+h,b+h)-lag(e-h,b+h)-lag(e+h,b-h)+lag(e-h,b-h))/(4*h*h)
    check("lorentzian_good_and_bad_signs", abs(mixed-0.7) < 1e-10 and abs(-mixed-0.7) > 1)
    check("source_free_zero_field_control", lag(0, 0) == 0 and -2*0*0 == 0)
    check("perfect_mirror_degeneracy", all(-2*(-x)*x == 2*x*x for x in (-0.4, 0.1, 2)))

    # A divergence of an antisymmetric derivative vanishes on commuting stencils.
    # This checks the conservation identity only. No microscopic current is supplied.
    def dx(f, x, y):
        return (f(x+h, y)-f(x-h, y))/(2*h)
    def dy(f, x, y):
        return (f(x, y+h)-f(x, y-h))/(2*h)
    def potential(x, y):
        return x*x*y + 2*x*y*y
    divergence = (dx(lambda x,y: dy(potential,x,y), 0.2, 0.3)
                  - dy(lambda x,y: dx(potential,x,y), 0.2, 0.3))
    check("induced_current_divergence_identity", abs(divergence) < 1e-11)
    record["status"] = "PASS_SCOPED_ARCHIVE_AND_ALGEBRA"
except Exception as exc:
    record.update(status="HOLD", error=f"{type(exc).__name__}: {exc}")
finally:
    record.update(checks=checks, wall_s=time.perf_counter()-wall, cpu_s=time.process_time()-cpu,
                  new_coupled_solves=0, full_regression="FULL_REGRESSION_PENDING",
                  next="NO_AUTOMATIC_PROMOTION")
    raw = (json.dumps(record, indent=2, sort_keys=True)+"\n").encode()
    with (out/"verification.json").open("xb") as f:
        f.write(raw)
    with (out/"verification.json.sha256").open("x") as f:
        f.write(f"{digest(raw)}  verification.json\n")
    print("F0_VERIFICATION=" + record["status"])
    print("VERIFICATION_JSON=" + str(out/"verification.json"))
    print("VERIFICATION_SHA256=" + digest(raw))
    if "error" in record:
        print("ERROR=" + record["error"])
raise SystemExit(0 if record["status"].startswith("PASS_") else 1)
