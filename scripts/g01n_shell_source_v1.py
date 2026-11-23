"""G01-N. Static dipole source fork in the R3X1 leading-trace theory."""
from pathlib import Path
import hashlib, json, math, sys
import mpmath as m

root, out = map(Path, sys.argv[1:])
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
gap = "results/gravity2/r3b_gap_preflight_v1/"
r3b = "results/data/032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json"
b1 = "results/data/032h17a12d1r3x3b1_portal_scale_physical_preflight.json"
pins = {
    r3b: "9474b6782104abb5bd8dd5e893137621b30ad96109e3e52c5a01268794810b11",
    b1: "dff7ba4cb6459ba381c84173416cd0192def9c22bf3b1b2c3dd5889d00cf2b2f",
    gap+"science.json": "d5e0f8ac515e2247cce2b2c252136e9aea140c7973d8b0820c3e6d3db94f522e",
    gap+"verification.json": "2d4b116fd7e8693eac9e314e697e68364ac190262465e25ae92119af8f332396",
    gap+"produce.py": "03aea50b83249a222eeef9ca3dd741f48e0e29a45ddb3a7469ebb161f8bc914e",
    gap+"verify.py": "a936c192cdf6379cfc6a76373e37612a9797eae195b2d1b0ea2429ac962161d8",
    "src/antigravity_research/agminer/hook17_fdual_f_r3x1_lorentzian_sign_audit.py":
        "6f1bf0922712a81e860075a71201af49c7870fa18fe2c21e7f576bb46da97531",
}
for name, expected in pins.items():
    if sha(root/name) != expected:
        raise SystemExit("PARENT SHA MISMATCH "+name)
read = lambda name: json.loads((root/name).read_bytes())
g = read(r3b)["grid_results"]["0.05"]
norm = (g["payload_reconstruction"]["normalized_mixed_global_field_energy_j"]
        / g["global_energy"]["mixed_global_field_energy_before_1g_renormalization_j"])
u_ref = norm*g["multipole_modes"][0]["electric_exterior_energy_j"]
masses = [1000., 1000.*read(b1)["grids"][0]["rows"][0]["M_X_keV"]]
m.mp.dps = 65
I = m.eye(2)
eps0, c, R, rho = 8.8541878128e-12, 299792458., 2., 2200.
unit = 1.602176634e-19/(1.973269804e-7)**3

def transfer(theta, p, f):
    # f = fraction of sphere volume occupied by the shell.
    # Potentials of E and H; normal fluxes are D and B.
    M = m.matrix([[p+theta**2, theta], [theta, 1]])
    C = (2*M+I)**-1*(M-I)
    W = (1-f)*C
    A = M*(I-2*W)
    return A*(2*(I+W)+A)**-1

rows = []
for mass in masses:
    theta = m.mpf(2*rho*c*c/(unit*mass**4))
    ue = u_ref*(mass/1000.)**4
    field = math.sqrt(3*ue/(math.pi*eps0*R**3))
    for p in (1., 3.8):
        def mirror(f):
            G = transfer(theta, p, f)
            return 1-G[0,0]-G[1,0]
        lo, hi = m.mpf(0), m.mpf(1)
        if not mirror(lo)>0>mirror(hi):
            raise ValueError("Missing electric dipole root in physical interval")
        for _ in range(100):
            mid = (lo+hi)/2
            if mirror(mid)>0:
                lo = mid
            else:
                hi = mid
        f = (lo+hi)/2
        G = transfer(theta, p, f)
        # Auxiliary optical screen only for an achromatic bright-X extension.
        n_x, n_y = 1.46, 1.
        admittance = n_x + float(theta)**2/(1+n_y)
        gain = 1-G[0,0]
        rows.append(dict(scale_eV=mass, eps_r=p, theta=float(theta),
            shell_fraction=float(f), shell_mass_kg=float(4*math.pi*R**3*rho*f/3),
            optical_halfspace_Rxx_if_achromatic=((1-admittance)/(1+admittance))**2,
            thickness_m=float(R*(1-(1-f)**(m.mpf(1)/3))),
            magnetic_drive_E_over_cB=float(G[0,1]/G[1,1]),
            electric_drive_cB_over_E=float(-G[1,0]/gain),
            E_pole_V_m=field, surface_charge_peak_C_m2=float(eps0*field/gain),
            exterior_electric_dipole_J=ue, all_space_static_field_J=float(ue/gain)))
science = dict(run="G01-N", parents=pins, producer_sha256=sha(Path(__file__)),
    model="static dipole, 2 m vacuum-core spherical shell, fixed free charge or current sheet",
    convention="D=pE+theta*cB; H=cB-theta*E in normalized units; sigma proportional to -E.cB",
    optical_control="normal incidence, one vacuum interface, n_X=1.46, n_Y=1, mu=1, constant theta",
    material="assumed constant density 2200 kg/m3, ordinary bright carrier, unit hidden susceptibility",
    scale_transfer="same fine-parent exterior dipole metric amplitude; B1 supplies scale only",
    result="CHARGE_DRIVEN_EXTERNAL_DIPOLE_MATCH_CONDITIONAL", rows=rows,
    physical_survivors=0, loaded_payload="UNSOLVED", Earth_craft="UNSOLVED",
    complete_energy="UNKNOWN", full_regression="NOT_RUN")
with (out/"science.json").open("x") as stream:
    json.dump(science, stream, sort_keys=True, indent=2, allow_nan=False)
    stream.write("\n")
for row in rows:
    print(row, flush=True)
print("SCIENCE_SHA256", sha(out/"science.json"))
