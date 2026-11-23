"""G01-T3: fine-grid, 10 MJ, exact quadratic dual certificate.

Uses the immutable G01-T2 quadratic coefficients.

The nonnegative weights are an independently discovered
numerical dual witness. The calculation checks whether
they prove an energy-bounded obstruction for all ten-mode
shell-control amplitudes, without a nonlinear optimizer.

This is NOT a physical-source or gravitational-device claim.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

parent = Path(sys.argv[1])
out = Path(sys.argv[2])

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

expected_science = (
    "8f4e5b27b7b84372bdeb2727f3e37eef270b8ea959754d4f3d9a4f806e3e5ed6"
)
expected_coefficients = (
    "0296771603d17f1b60b1a790f1a8b46e21c0471fe7e7bbe0d2be273c7b61c962"
)

science = parent / "science.json"
coeff = parent / "quadratic_coefficients.npz"

assert sha(science) == expected_science
assert sha(coeff) == expected_coefficients

original = json.loads(science.read_text())
assert original["experiment"].startswith("G01-T2-")

z = np.load(coeff, allow_pickle=False)

a0 = z["a0_050"]
g = z["g_050"]
Q = z["Q_050"]
K = z["K_050"]
ell = z["l_050"]
E0 = float(z["E0_050"])

# Witness discovered from the original 48-point fine grid.
w = np.array([
    0.0000000001, 0.0000708292, 0.0000074150, 0.0000000000,
    0.0541769665, 0.0037405810, 0.0590870306, 0.0000000000,
    0.0001454715, 0.0047618177, 0.0185307530, 0.0668086319,
    0.1119036788, 0.0078062201, 0.0010259253, 0.0030465307,
    0.0015330376, 0.0006243880, 0.0131655578, 0.0227410198,
    0.0025562052, 0.0000377496, 0.0007696037, 0.0000010897,
    0.0151122247, 0.0015169442, 0.0151118778, 0.0847285598,
    0.0003945233, 0.0843302398, 0.0017072501, 0.0127621161,
    0.0163572832, 0.0590923566, 0.0043408908, 0.0947768010,
    0.0000000227, 0.0482785409, 0.0659168812, 0.0000000000,
    0.0521877332, 0.0705156596, 0.0001610568, 0.0000000000,
    0.0000000000, 0.0000000000, 0.0001655109, 0.0000030245,
], dtype=float)

assert w.shape == (48,)
assert np.all(w >= 0)
w /= w.sum()

cap = 10000000.0
target = 9.80665
lam = 5e-7

Qw = np.einsum("i,ijk->jk", w, Q)
M = lam * K - Qw
M = 0.5 * (M + M.T)

eigen = np.linalg.eigvalsh(M)
minimum_eigen = float(eigen[0])

assert minimum_eigen > 1e-7
np.linalg.cholesky(M)

b = w @ g - lam * ell

upper = float(
    w @ a0
    + lam * (cap - E0)
    + 0.25 * b @ np.linalg.solve(M, b)
)

# Independent spectral reconstruction of the quadratic term.
values, vectors = np.linalg.eigh(M)

spectral_upper = float(
    w @ a0
    + lam * (cap - E0)
    + 0.25 * np.sum((vectors.T @ b)**2 / values)
)

assert abs(upper - spectral_upper) < 1e-7
assert upper < target - 1.0

out.mkdir(parents=True, exist_ok=False)

result = {
    "experiment": "G01-T3-FINE-GRID-ENERGY-CAP-CERTIFICATE",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "parent_science_sha256": expected_science,
    "parent_coefficients_sha256": expected_coefficients,
    "producer_sha256": sha(Path(__file__)),
    "field_energy_cap_j": cap,
    "lambda": lam,
    "weights": w.tolist(),
    "weight_sum": float(w.sum()),
    "minimum_weight": float(w.min()),
    "dual_matrix_minimum_eigenvalue": minimum_eigen,
    "acceleration_upper_bound_m_s2": upper,
    "independent_spectral_upper_bound_m_s2":
        spectral_upper,
    "required_m_s2": target,
    "certificate_pass": bool(upper < target),
    "scope": (
        "FINE_GRID_48_POINTS_TEN_ORIGINAL_SHELL_MODES_"
        "FROZEN_BETA_POSITIVE_CANONICAL_FIELD_ENERGY"
    ),
    "full_regression": "NOT_RUN",
    "second_field_solver": "NOT_RUN",
    "source_action": "NOT_IDENTIFIED",
    "universal_gravity": "NOT_DERIVED",
    "whole_craft_lift": "NOT_DERIVED",
    "physical_survivors": 0,
}

raw = (
    json.dumps(result, sort_keys=True, indent=2)
    + "\n"
).encode()

with (out / "certificate.json").open("xb") as f:
    f.write(raw)

with (out / "certificate.json.sha256").open("x") as f:
    f.write(
        hashlib.sha256(raw).hexdigest()
        + "  certificate.json\n"
    )

print("G01T3_DUAL_CERTIFICATE=PASS")
print("FINE_GRID_ONLY=YES")
print("MINIMUM_EIGENVALUE=", minimum_eigen)
print("MAXIMUM_ALLOWED_MINIMUM_ACCELERATION=", upper)
print("TARGET=", target)
print("TEN_MODE_10MJ_RESCUE=EXCLUDED_IN_SCOPED_MODEL")
print("PHYSICAL_SOURCE=NOT_IDENTIFIED")
print("CERTIFICATE_SHA256=", hashlib.sha256(raw).hexdigest())
