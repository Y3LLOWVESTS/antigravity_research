"""G01-T artifact and negative-control verification.

This checks independent artifact integrity, signed-parent
reproduction, optimizer bounds and conservative claim gates.
It is not an independent G01-T field solver.
"""

import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]).resolve()

if ROOT not in OUT.parents or not OUT.is_dir():
    raise SystemExit("BAD_OUTPUT_DIRECTORY")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


raw = (OUT / "science.json").read_bytes()

recorded = (
    (OUT / "science.json.sha256")
    .read_text().strip().split()[0]
)

assert sha(OUT / "science.json") == recorded

data = json.loads(raw)

assert data["experiment"] == "G01-T0T1"
assert data["source_sha256"] == sha(
    ROOT / "scripts/g01t_t0t1.py"
)

for relative, expected in data["parents"].items():
    assert sha(ROOT / relative) == expected, relative

assert data["physical_qualified_survivors"] == 0
assert data["source_action_identified"] is False
assert data["neutral_matter_equilibrium_varied"] is False
assert data["earth_craft_Einstein_force_derived"] is False
assert data["operating_energy_certified"] is False

assert len(data["grids"]) == 2

expected_baselines = {
    0.075: -46.4060741,
    0.050: -129.67185782242464,
}

for grid in data["grids"]:
    h = grid["h_m"]
    target = expected_baselines[h]

    assert abs(
        grid["original_loaded_min_m_s2"] - target
    ) < 0.15

    assert grid["original_relative_residual"] < 1e-7
    assert grid["lorentzian_coupling_signs"] == [1, -1]

    assert (
        grid["sampled_min_shell_clearance_m"]
        >= 1.0 - 2.0 * h
    )

    assert (
        grid["no_electric_monopole_quadrature_max_error"]
        < 1e-12
    )

    modes = grid["control_modes"]

    assert len(modes) == 10
    assert len(
        grid["loaded_response_singular_values_m_s2_per_sqrt_j"]
    ) == 10

    assert 0 <= (
        grid["loaded_response_rank_at_rel_1e_8"]
    ) <= 10

    for mode in modes:
        assert mode["raw_loaded_energy_j"] > 0
        assert mode["signed_static_residual"] < 2e-6
        assert mode["physical_Y_source_identified"] is False

    rows = grid["rows"]

    assert len(rows) == 5
    assert [r["mode_bound"] for r in rows] == [
        0.0, 0.25, 0.5, 1.0, 2.0
    ]

    assert all(r["success"] for r in rows)

    zero = rows[0]

    assert abs(
        zero["linearized_min_m_s2"] - target
    ) < 0.15

    assert abs(
        zero["full_bilinear_min_m_s2"] - target
    ) < 0.15

    assert math.isclose(
        zero["full_bilinear_field_energy_j"],
        grid["original_loaded_energy_j"],
        rel_tol=1e-9,
        abs_tol=1e-7,
    )

    for row in rows:
        assert len(row["controls"]) == 10

        assert all(
            abs(c) <= row["mode_bound"] + 1e-8
            for c in row["controls"]
        )

        assert math.isfinite(
            row["full_bilinear_min_m_s2"]
        )

        assert math.isfinite(
            row["full_bilinear_field_energy_j"]
        )

        assert row["full_bilinear_field_energy_j"] > 0

        assert row["physical_source_gate"].startswith(
            "HOLD"
        )

        assert row["physical_gravity_gate"] == (
            "NOT_EVALUATED"
        )

    if h == 0.075:
        assert (
            grid["direct_sparse_parent_validation"]["pass"]
            is True
        )

print("G01_T_ARTIFACT_AND_NEGATIVE_CONTROLS=PASS")
print("INDEPENDENT_G01T_FIELD_SOLVER=NOT_RUN")
print("SOURCE_ACTION=NOT_IDENTIFIED")
print("FULL_GRAVITATIONAL_BRIDGE=NOT_DERIVED")
print("SCIENCE_SHA256=" + recorded)
