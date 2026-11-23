from pathlib import Path
import hashlib, json, math, sys
import numpy as np
from numpy.polynomial.legendre import Legendre, leggauss

d = Path(__file__).parent
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
parent = Path(sys.argv[1])
s = json.loads((d/"science.json").read_text())
pin = "9474b6782104abb5bd8dd5e893137621b30ad96109e3e52c5a01268794810b11"
assert sha(parent) == s["parent_sha256"] == pin
assert sha(d/"produce.py") == s["producer_sha256"]
grids = json.loads(parent.read_text())["grid_results"]
errors = []
for n in (32, 64):
    x, w = leggauss(n)
    radius = (2.5 + x/2)[:, None]
    for h, grid in grids.items():
        br = np.zeros((n,n))
        bt = np.zeros_like(br)
        for row in grid["multipole_modes"]:
            l = row["ell"]
            P = Legendre.basis(l)
            a = row["boundary_scalar_amplitude"] * (2/radius)**(l+1) / radius
            br += (l+1)*a*P(x)
            bt += a*np.sqrt(1-x*x)*P.deriv()(x)
        scale = (grid["payload_reconstruction"]["normalized_mixed_global_field_energy_j"]
                 / grid["global_energy"]["mixed_global_field_energy_before_1g_renormalization_j"])
        # Both fitted carriers have amplitude |B_fit|/sqrt(2).
        u = 0.5*(br*br + bt*bt)*scale*(1.602176634e-19/1.973269804e-7)
        gap = float(math.pi * (w @ (radius**2 * u) @ w))
        errors.append(abs(gap-s["fitted_preload_gap_J"][h]))
    # Coulomb control in Gaussian units. Two +1 charges, z=0 and z=5.
    # Surface traction on the first charge must equal -1/25 at every radius.
    for r in (2.0, 2.5, 3.0):
        dist = np.sqrt(r*r + 25 - 10*r*x)
        er = 1/r**2 + (r-5*x)/dist**3
        et = 5*np.sqrt(1-x*x)/dist**3
        tz = 0.5*x*(er**2-et**2) - np.sqrt(1-x*x)*er*et
        assert abs(r*r*(w @ tz)/2 + 1/25) < 1e-10
assert max(errors) < 1e-11 and s["static_two_body_Maxwell_floor_J"] == 1*9.80665*1
report = dict(status="PASS_SCOPED", science_sha256=sha(d/"science.json"),
              verifier_sha256=sha(Path(__file__)), max_gap_error_J=max(errors))
with (d/"verification.json").open("x") as f:
    json.dump(report, f, sort_keys=True, indent=2)
    f.write("\n")
print(report, "verification_sha256", sha(d/"verification.json"))
