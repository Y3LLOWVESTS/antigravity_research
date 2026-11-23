"""Independent G01-T2 quadratic and dual-certificate audit.

No full repository regression and no second field solve.
This independently checks saved mathematical coefficients,
historical results, source fingerprints and the dual bound.
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import solve_triangular

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]).resolve()

if ROOT not in OUT.parents or not OUT.is_dir():
    raise RuntimeError("INVALID_OUTPUT_LOCATION")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def a_values(G, u):
    return (
        G["a0"] + G["g"] @ u
        + np.einsum(
            "i,nij,j->n", u, G["Q"], u, optimize=True
        )
    )


def energy(G, u):
    return float(
        G["E0"] + G["l"] @ u + u @ G["K"] @ u
    )


science = OUT / "science.json"
d = json.loads(science.read_text())

recorded_sha = (
    OUT / "science.json.sha256"
).read_text().split()[0]

assert sha(science) == recorded_sha

assert d["experiment"] == (
    "G01-T2-EXACT-QUADRATIC-SHARED-SOURCE-GOLDEN"
)

assert sha(
    ROOT / "scripts/g01t2_golden_exact.py"
) == d["source_sha256"]

assert sha(
    OUT / d["quadratic_coefficients_file"]
) == d["quadratic_coefficients_sha256"]

assert sha(
    ROOT / "scripts/g01t_t0t1.py"
) == d["t1_source_sha256"]

for filename, expected in d["parent_files_sha256"].items():
    assert sha(ROOT / filename) == expected, filename

pointer = (
    ROOT / "results/gravity2/G01T_LATEST_PATH.txt"
)

t1path = (
    ROOT / pointer.read_text().strip() / "science.json"
)

assert sha(t1path) == d["t1_science_sha256"]

t1 = json.loads(t1path.read_text())

z = np.load(
    OUT / "quadratic_coefficients.npz",
    allow_pickle=False,
)

grids = []

for tag, result in zip(
    ("075", "050"), d["grids"]
):
    G = {
        name: z[f"{name}_{tag}"]
        for name in ("a0", "g", "Q", "E0", "l", "K")
    }

    assert np.allclose(
        G["Q"], np.swapaxes(G["Q"], 1, 2),
        atol=1e-11,
    )

    assert min(np.linalg.eigvalsh(G["K"])) > 0

    assert len(G["a0"]) == result["payload_count"]

    assert abs(
        float(np.min(G["a0"]))
        - result["baseline_min_m_s2"]
    ) < 1e-6

    assert result["minimum_sampled_clearance_m"] >= 1.0

    grids.append(G)

coarse_norm = np.sqrt(
    np.asarray(
        d["grids"][0]["raw_loaded_mode_energy_j"]
    )
)

for G, result, old in zip(
    grids, d["grids"], t1["grids"]
):
    factors = (
        coarse_norm
        / np.sqrt(np.asarray(
            result["raw_loaded_mode_energy_j"]
        ))
    )

    for row in old["rows"]:
        if not row["success"]:
            continue

        u = np.asarray(row["controls"]) * factors

        assert abs(
            float(np.min(a_values(G, u)))
            - row["full_bilinear_min_m_s2"]
        ) < 1e-6

        assert abs(
            energy(G, u)
            - row["full_bilinear_field_energy_j"]
        ) < 1e-7

for row in d["results"]:
    if row["best"] is None:
        continue

    best = row["best"]
    u = np.asarray(best["u"])

    cap = row["cap_canonical_field_j"]
    bound = row["bound_per_coarse_normalized_mode"]

    assert u.shape == (10,)
    assert np.max(np.abs(u)) <= bound + 1e-6

    accelerations = [
        float(np.min(a_values(G, u)))
        for G in grids
    ]

    energies = [
        energy(G, u)
        for G in grids
    ]

    assert max(energies) <= cap + 2e-6

    assert abs(
        min(accelerations) - best["min_m_s2"]
    ) < 2e-5

    assert max(
        abs(a - b)
        for a, b in zip(
            energies, best["field_energy_j_by_grid"]
        )
    ) < 1e-6

# Independently recompute each recorded dual upper bound.
for diagnostic in d["rigorous_relaxed_energy_ball_bounds"]:
    cap = diagnostic["field_energy_cap_j"]
    values = []

    for item, G in zip(
        diagnostic["per_grid"], grids
    ):
        j = item["payload_index"]
        lam = item["certifying_dual_lambda"]

        K = G["K"]
        Q = G["Q"][j]
        grad = G["g"][j]

        uc = -0.5 * np.linalg.solve(K, G["l"])
        emin = energy(G, uc)

        assert cap > emin

        U = np.linalg.cholesky(K).T

        invU = solve_triangular(
            U, np.eye(10), lower=False
        )

        H = invU.T @ Q @ invU
        H = (H + H.T) / 2

        eig, V = np.linalg.eigh(H)

        assert lam > max(0.0, float(eig[-1]))

        new_grad = invU.T @ (grad + 2 * Q @ uc)

        constant = float(
            G["a0"][j]
            + grad @ uc
            + uc @ Q @ uc
        )

        dual = float(
            constant
            + lam * (cap - emin)
            + 0.25 * np.sum(
                (V.T @ new_grad) ** 2 / (lam - eig)
            )
        )

        recorded = item[
            "energy_ellipsoid_dual_upper_m_s2"
        ]

        assert abs(dual - recorded) < (
            1e-5 * max(1.0, abs(dual))
        )

        values.append(dual)

    joint = min(values)

    assert abs(
        joint - diagnostic["joint_optimistic_upper_m_s2"]
    ) < 1e-5 * max(1.0, abs(joint))

    if cap == 10000.0:
        assert joint < d["target_m_s2"] - 0.01

assert d["physical_survivors"] == 0
assert d["full_regression"] == "NOT_RUN_BY_USER_POLICY"
assert d["physical_source_action"] == "NOT_DERIVED"
assert d["earth_down_whole_craft_up"] == "NOT_DERIVED"

print("G01T2_QUADRATIC_INDEPENDENT=PASS")
print("G01T2_T1_NUMERICAL_REPRODUCTION=PASS")
print("G01T2_ENERGY_DUAL_CERTIFICATE=PASS")
print("G01T2_SHARED_SHELL_CONTROLS=PASS")
print("G01T2_FULL_REGRESSION=NOT_RUN")
print("G01T2_SECOND_FIELD_SOLVER=NOT_RUN")
print(
    "OPTIMISTIC_NECESSARY_FIELD_ENERGY_J=",
    d["optimistic_necessary_field_energy_j_for_sampled_1g"],
)
print("PHYSICAL_GRAVITATIONAL_SURVIVOR=NO")
print("SCIENCE_SHA256=" + sha(science))
