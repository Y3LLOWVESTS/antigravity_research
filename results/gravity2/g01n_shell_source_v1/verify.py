"""Independent two-interface matching in E and cB, with energy integrated by region."""
from pathlib import Path
import hashlib, json, sys
import mpmath as m

root, out = map(Path, sys.argv[1:])
m.mp.dps = 75
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
science = json.loads((out/"science.json").read_bytes())
def check(ok, why):
    if not ok:
        raise ValueError(why)

check(sha(out/"produce.py")==science["producer_sha256"], "producer drift")
for name, expected in science["parents"].items():
    check(sha(root/name)==expected, "parent drift "+name)

def direct(a, p, z, drive):
    # x=r/R. Potentials of E and cB are cr, ur+v/r^2, and w/r^2.
    def jumps(coeff):
        c, u, v, w = [coeff[i:i+2,:] for i in (0,2,4,6)]
        def surface(en, et, bn, bt, eps, th):
            return m.matrix([et, bn, eps*en+th*bn, bt-th*et])
        def traces(n, t, eps, th):
            return surface(n[0], t[0], n[1], t[1], eps, th)
        inside = traces(-c,c,1,0)
        layer = lambda x: traces(-u+2*v/x**3,u+v/x**3,p,z)
        exterior = traces(2*w,w,1,0)
        return m.matrix(list(layer(a)-inside)+list(exterior-layer(1)))
    mat = m.matrix(8)
    for j in range(8):
        mat[:,j] = jumps(m.eye(8)[:,j])
    rhs = m.matrix(8,1)
    rhs[6 if drive=="charge" else 7] = 1
    return m.lu_solve(mat,rhs)

def close(x,y,tol="2e-11"):
    check(abs(x-y)<=m.mpf(tol)*max(abs(y),m.mpf("1e-40")), "numerical mismatch")

eps0 = m.mpf("8.8541878128e-12")
unit = m.mpf("1.602176634e-19")/m.mpf("1.973269804e-7")**3
r3b = next(k for k in science["parents"] if k.endswith("global_mirror_prefight_summary.json"))
g = json.loads((root/r3b).read_bytes())["grid_results"]["0.05"]
amplitude = g["multipole_modes"][0]["boundary_scalar_amplitude"]
norm = (g["payload_reconstruction"]["normalized_mixed_global_field_energy_j"]
        /g["global_energy"]["mixed_global_field_energy_before_1g_renormalization_j"])
u0 = 2*m.pi*2*(2*m.mpf(amplitude)**2/3)*m.mpf("1.602176634e-19")/m.mpf("1.973269804e-7")*norm/2
rows = []
expected_scales = {1000., 1000.*json.loads((root/next(k for k in science["parents"]
    if k.endswith("portal_scale_physical_preflight.json"))).read_bytes())["grids"][0]["rows"][0]["M_X_keV"]}
check(len(science["rows"])==4 and {(r["scale_eV"],r["eps_r"]) for r in science["rows"]}
      == {(s,p) for s in expected_scales for p in (1.,3.8)}, "missing or duplicate row")
for r in science["rows"]:
    p = m.mpf(r["eps_r"])
    mass = m.mpf(r["scale_eV"])
    z = 2*2200*299792458**2/(unit*mass**4)
    a = 1-m.mpf(r["thickness_m"])/2
    close(z, r["theta"])
    # Transmitted electric amplitudes in orthogonal polarizations of X,Y.
    tx,ty = m.lu_solve(m.matrix([["2.46",z],[-z,2]]), m.matrix([2,0]))
    close((tx-1)**2,r["optical_halfspace_Rxx_if_achromatic"])
    close((tx-1)**2+ty**2+m.mpf("1.46")*tx**2+ty**2,1)
    close(4*m.pi*8*2200*(1-a**3)/3,r["shell_mass_kg"])
    close(1-a**3, r["shell_fraction"])
    ue = u0*(mass/1000)**4
    close(ue, r["exterior_electric_dipole_J"])
    v = direct(a,p,z,"charge")
    mag = direct(a,p,z,"current")
    close(v[7]/v[6], -1)
    close(v[7]/v[6], r["electric_drive_cB_over_E"])
    close(mag[6]/mag[7], r["magnetic_drive_E_over_cB"])
    check(mag[6]/mag[7]>0, "magnetic drive sign")
    field = m.sqrt(3*ue/(m.pi*eps0*8))
    close(field,r["E_pole_V_m"])
    strength = field/(2*v[6])
    close(eps0*strength,r["surface_charge_peak_C_m2"])
    c,u,b,w = [(v*strength)[i:i+2,:] for i in (0,2,4,6)]
    # Angular integration cancels the growing/decaying cross terms.
    norm2 = lambda x,ep: ep*x[0]**2+x[1]**2
    integral = (a**3*norm2(c,1)+(1-a**3)*norm2(u,p)
                +2*(a**-3-1)*norm2(b,p)+2*norm2(w,1))
    energy = 2*m.pi*eps0*8/3*integral
    close(energy,r["all_space_static_field_J"])
    # Field-component extrema in the homogeneous layer occur at its two faces.
    faces = [s for x in (a,1) for s in (-u+2*b/x**3,u+b/x**3)]
    emax = max(abs(s[0]) for s in faces)
    cbmax = max(abs(s[1]) for s in faces)
    sigma_bound = 2*eps0*emax*cbmax/(unit*mass**4)
    check(sigma_bound<m.mpf("1e-5"), "weak conformal expansion requires review")
    rows.append(dict(scale_eV=float(mass),eps_r=float(p),
        field_volume_J=float(energy),max_shell_E_V_m=float(emax),
        max_shell_hidden_cB_V_m=float(cbmax),weak_abs_sigma_upper=float(sigma_bound)))
# Interface and sign controls, including exact no-conversion in vacuum.
a = m.mpf("0.75")
for drive in ("charge","current"):
    v0 = direct(a,1,0,drive)
    close(v0[7 if drive=="charge" else 6],0)
    plus,minus = [direct(a,1,z,drive) for z in (2,-2)]
    cross = 7 if drive=="charge" else 6
    close(plus[cross],-minus[cross])
    close(plus[13-cross],minus[13-cross])
report = dict(status="PASS_SCOPED_SOURCE_BOUNDARY_PROBLEM", verifier_sha256=sha(Path(__file__)),
    science_sha256=sha(out/"science.json"), checks=rows, full_regression="NOT_RUN")
with (out/"verification.json").open("x") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
print(json.dumps(report,indent=2))
print("VERIFICATION_SHA256",sha(out/"verification.json"))
