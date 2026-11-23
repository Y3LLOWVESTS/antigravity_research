from pathlib import Path
import hashlib, json, sys

parent = Path(sys.argv[1])
raw = parent.read_bytes()
digest = lambda data: hashlib.sha256(data).hexdigest()
if digest(raw) != "9474b6782104abb5bd8dd5e893137621b30ad96109e3e52c5a01268794810b11":
    raise SystemExit("R3B parent SHA mismatch")
rows = {}
for h, grid in json.loads(raw)["grid_results"].items():
    e = grid["global_energy"]
    scale = (grid["payload_reconstruction"]["normalized_mixed_global_field_energy_j"]
             / e["mixed_global_field_energy_before_1g_renormalization_j"])
    total = 0.0
    for mode in grid["multipole_modes"]:
        outside = mode["electric_exterior_energy_j"] + 0.5 * mode["magnetic_exterior_energy_j"]
        total += scale * outside * (1 - (2/3)**(2*mode["ell"] + 1))
    rows[h] = total
result = dict(parent_sha256=digest(raw), producer_sha256=digest(Path(__file__).read_bytes()),
              fitted_preload_gap_J=rows, static_two_body_Maxwell_floor_J=9.80665,
              physical_survivors=0, full_regression="NOT_RUN")
out = Path(__file__).with_name("science.json")
with out.open("x") as f:
    json.dump(result, f, sort_keys=True, indent=2, allow_nan=False)
    f.write("\n")
print(out, digest(out.read_bytes()))
