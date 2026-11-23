"""G01-O. Is the G01-N charged dipole both sourceable and compatible with a silica-sphere control?

Canonical electric sectors are a spectator photon and X. A single ordinary
electric charge has direction n=(sqrt(1-s),sqrt(s)); Y has no free charge.
Ordinary electric susceptibility is (eps-1) n n^T, eps>=1. Magnetic
permeabilities and hidden dielectric susceptibility are unity. In the G01-N
static material law the mixed coefficient theta is proportional to density.
Vacuum surrounds the bead, and the incident field is purely ordinary. These
are hypotheses; a laboratory apparatus containing the same portal can change
the incident fields, force gradients, and calibration.

All laboratory numbers come from Rider et al., PRL 117, 101101 (2016), Table I
and the quoted manufacturer radius spread. The envelope is an explicit
sensitivity calculation, not a statistical exclusion. Energy is total vacuum
exterior dipole energy in joules, assuming activation from zero fields. The
paper reference normalizes to eps_ref=3 and r_ref=2.5 micrometres.
"""
import hashlib
import json
import sys
import tarfile
from pathlib import Path

root, out = map(Path, sys.argv[1:3])
digest = lambda b: hashlib.sha256(b).hexdigest()
base = root / "results/gravity2"
parent = base / "g01n_shell_source_v1"
archive = base / "g01n_shell_source_v1_UPLOAD.tar.gz"
archive_sha = "a1f9b4dbb374c2e857c2efacf1965436c3b52779f8967766b8bcb4f8ad3c8be4"
if digest(archive.read_bytes()) != archive_sha:
    raise ValueError("Run 2 archive drift")
with tarfile.open(archive, "r:gz") as bundle:
    def member(name):
        return bundle.extractfile(parent.name + "/" + name).read()
    ledger = dict(line.split()[::-1] for line in member("SHA256SUMS.txt").decode().splitlines())
    expected_files = {"science.json","verification.json","produce.py","verify.py","produce.log","verify.log"}
    if set(ledger) != expected_files:
        raise ValueError("Run 2 ledger inventory")
    for name, expected in ledger.items():
        if digest(member(name)) != expected or digest((parent/name).read_bytes()) != expected:
            raise ValueError("Run 2 ledger drift: "+name)
parent_data = json.loads((parent/"science.json").read_bytes())
for name, pin in parent_data["parents"].items():
    if digest((root/name).read_bytes()) != pin:
        raise ValueError("Run 2 upstream drift: "+name)

# Each pair is alpha/alpha0 and its reported uncertainty.
beads = [(0.21, 0.13), (0.00, 0.33), (0.25, 0.14)]
radius_ratio = (2.50-3*0.24)/2.50
upper = min(center+3*spread for center, spread in beads)
rho_lab_min = 1000.0
budget = 1e7
rows = []
for r in parent_data["rows"]:
    if r["eps_r"] != 3.8:
        continue
    z = r["theta"]
    u = r["exterior_electric_dipole_J"]
    if z <= 3 or not 0 < 2*u < budget:
        raise ValueError("source theorem domain")
    z_lab = z*rho_lab_min/2200.
    bead_floor = 2*z_lab*z_lab/(9+2*z_lab*z_lab)
    s_max = 0.4*upper/(radius_ratio**3*bead_floor)
    # For every shell fraction yielding B_Y=-E_X, f>=3/z. The spectator
    # field at the pole is E_X*sqrt((1-s)/s)*(1+2*f*z^2/9).
    spectator_factor = (1+2*z/3)**2
    s_min = spectator_factor/(spectator_factor+budget/u-2)
    exterior_floor = u*(2+spectator_factor*(1-s_max)/s_max)
    lab_floor = radius_ratio**3*bead_floor*s_min/0.4
    rows.append(dict(portal_scale_eV=r["scale_eV"], theta=z,
        reference_exterior_electric_J=u, lab_s_max=s_max, energy_s_strict_min=s_min,
        vacuum_exterior_J_at_lab_bound_lower=exterior_floor,
        minimum_alpha_over_alpha0_at_energy_bound=lab_floor,
        maximum_apparent_response_multiplier_to_overlap=upper/lab_floor,
        overlap=bool(s_min<s_max)))
if len(rows)!=2 or any(row["overlap"] for row in rows):
    raise ValueError("unexpected result; review the gate before publication")
report = dict(run="G01-O", archive_sha256=archive_sha, parent_science_sha256=ledger["science.json"],
    producer_sha256=digest(Path(__file__).read_bytes()), rows=rows, budget_J=budget,
    publication="https://doi.org/10.1103/PhysRevLett.117.101101",
    laboratory=dict(measured_alpha_over_alpha0=beads, reference_radius_um=2.5,
        radius_spread_um=0.24, chosen_min_radius_um=1.78,
        chosen_min_density_kg_m3=rho_lab_min, assumed_source_density_kg_m3=2200,
        apparent_ratio_ceiling=upper, ordinary_eps_min=1, sensitivity_multiples=3,
        ordinary_null_at_min_radius_eps3=radius_ratio**3),
    assumptions=["one ordinary electric charge direction in spectator-X plane",
        "no free Y drive or additional source currents; canonical vacuum fields",
        "passive ordinary electric permittivity >=1, unit magnetic and hidden response",
        "homogeneous layer, centered dipole, frozen leading trace, field-free off state",
        "Rider calibration and ordinary incident field transfer to the model",
        "local coefficient across laboratory and craft length scales"],
    decision="NO_OVERLAP_AT_TWO_PARENT_SCALES_CONDITIONAL_ON_LAB_TRANSFER",
    apparatus_self_consistent=False, model_independent_exclusion=False,
    physical_survivors=0, Earth_craft="UNSOLVED", complete_energy="UNCERTIFIED",
    full_regression="NOT_RUN")
with (out/"science.json").open("x") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
print(report["decision"])
for row in rows:
    print(row)
print("SCIENCE_SHA256",digest((out/"science.json").read_bytes()))
