"""DELTA1-F0. Audit archived R3B native-grid force and support evidence."""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

run = Path(__file__).resolve().parent
data = Path("results/data")
src = Path("src/antigravity_research/agminer")
b0 = data / "032h17a12d1r3x3b0_inverse_loading_summary.json"
b4 = data / "032h17a12d1r3x3b4_directional_com_summary.json"
mirror = data / "032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json"
delta = data / "delta1_02_20261120T172005211391Z.json"
prior = data / "delta1_02_verification_20261120T173340330519Z.json"
manifest_lock = "408e0f2eed8138097506fdee25508cf6cc4c375fe24fa8f79b615366e15161ed"
science_lock = "2feab292375dd33f7d97b66e71ad379ce9dd689dd4767052e06d68ede9850bb4"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write_new(name, raw):
    with (run / name).open("xb") as stream:
        stream.write(raw)

def encode(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()

def publish(name, raw):
    write_new(name, raw)
    write_new(name + ".sha256", f"{sha(raw)}  {name}\n".encode())

def require(condition, message):
    if not condition:
        raise ValueError(message)

wall, cpu = time.perf_counter(), time.process_time()
receipt = {
    "utc": datetime.now(timezone.utc).isoformat(),
    "producer_sha256": sha(Path(__file__).read_bytes()),
    "full_regression": "FULL_REGRESSION_PENDING",
    "pde_runs": 0,
}
try:
    paths = [b0, b4, mirror, delta, prior,
             Path("simulations/032h17a12d1r3x3b4_directional_com_quickcheck.py"),
             Path("src/antigravity_research/delta1/delta1_02_r3b_portal_rank.py")]
    paths += [src / name for name in (
        "hook17_f2_strong_payload_loading_rescue.py",
        "hook17_fdual_f_global_mirror_prefight.py",
        "hook17_fdual_f_r3x1_lorentzian_sign_audit.py",
        "hook17_fdual_f_r3x3b0_inverse_loading.py",
    )]
    for kind in ("focused", "full_regression", "independent"):
        paths.append(Path(f"results/logs/delta1_02_{kind}_20261120T171958125692Z.log"))

    # Parse the same bytes that were hashed, after the entire lock passes.
    raw = {p: p.read_bytes() for p in sorted(paths)}
    manifest = "".join(f"{sha(buf)}  {p.as_posix()}\n" for p, buf in raw.items()).encode()
    publish("parents.txt", manifest)
    require(len(raw) == 14 and sha(manifest) == manifest_lock, "PARENT_SHA_MISMATCH")
    r, force, m, d, v = [json.loads(raw[p]) for p in (b0, b4, mirror, delta, prior)]
    require(v["science_sha256"] == sha(raw[delta]), "DELTA1_02_PAIR_MISMATCH")
    require((v["focused_passed"], v["full_regression_passed"]) == (10, 3304),
            "HISTORICAL_REGRESSION_MISMATCH")
    require(not m["surface_charge_physicalized"] and
            not r["full_action_and_microscopic_currents_certified"] and
            not r["different_profile_same_metric_acceleration_excluded"], "SCOPE_CHANGED")
    require(d["original_R3B_prescribed_field_capacity_J"] == 1.5429162116460216 and
            m["provenance"]["a12c_field_energy_j"] == 2.6568591420597114, "CAPACITY_CHANGED")
    action = r["action"]
    require((action["positive_K_gauss_offdiagonal_sign"],
             action["positive_K_ampere_offdiagonal_sign"]) == (1, -1), "R3X1_SIGN")

    meshes, diagnostics = {}, {}
    for h in (0.075, 0.050):
        g, = [row for row in r["grids"] if row["h_m"] == h]
        f, = [row["fully_loaded"] for row in force["grids"] if row["h_m"] == h]
        native, = [row for row in d["native_meshes"] if row["grid_spacing_m"] == h]
        minimum = g["fully_loaded_min_a_m_s2"]
        require(g["full_load_direct_solver_pass"] and minimum < 0 and
                minimum == f["minimum_payload_acceleration_m_s2"], "LOADED_FORCE")
        require(f["force_identity_relative_error"] < 1e-10 and
                0 < f["positive_acceleration_mass_fraction"] < 1, "COM_IDENTITY")
        channels = g["inverse_counter_source"]["channels"]
        require(len(channels) == 2 and all(
            c["required_rhs_l2_unphysical_units"] > 0 and
            c["residual_l2_fraction_outside_buffered_support"] == 1
            for c in channels), "EXACT_MIRROR_SUPPORT")
        scan = {x["lambda"]: x for x in g["scalar_beta_suppression_diagnostic"]["scan"]}
        base = scan[0]
        slopes = []
        for step in (1e-9, 1e-8):
            row = scan[step]
            require(all(row[k] == base[k] for k in ("worst_rho_m", "worst_z_m")),
                    "INITIAL_ACTIVE_CELL_CHANGED")
            slopes.append((row["minimum_a_m_s2"] - base["minimum_a_m_s2"]) / step)
        require(min(slopes) > 0 and g["worst_payload_before"] != g["worst_payload_after"],
                "ACTIVE_CELL_DIAGNOSIS")
        key = f"{h:.3f}"
        meshes[key] = {
            "com_m_s2": f'{f["com_acceleration_m_s2"]:.8f}',
            "gap_m_s2": f"{9.80665 - minimum:.8f}",
            "min_m_s2": f"{minimum:.8f}",
        }
        diagnostics[key] = {
            "initial_secants_per_loading_fraction": slopes,
            "worst_rho_z_before_m": g["worst_payload_before"],
            "worst_rho_z_after_m": g["worst_payload_after"],
            "required_rhs_peak_radius_m": [c["required_rhs_peak_radius_m"] for c in channels],
            "original_beta_peak": native["peak_original_beta"],
            "prescribed_PQ_independent_fraction": native["gradient_independent_fraction_Q"],
            "interface_mean_sine": native["matter_interface_mean_misalignment_sin"],
        }

    science = dict(action="ACTION_INCOMPLETE", branch="DELTA1-F0",
                   complete_energy="ENERGY_UNDETERMINED", control="NO_NEW_PHYSICAL_CONTROL_TO_TEST",
                   earth_craft="NOT_DERIVED", frozen_beta="CORRECTED_FIELD_BLOCK_AVAILABLE",
                   loaded_operator="LOADED_RESPONSE_OPERATOR_UNAVAILABLE", meshes=meshes,
                   next="NO_AUTOMATIC_PROMOTION", outcome="F0_SOURCE_ACTION_UNDERDETERMINED",
                   parents_sha256=sha(manifest), scope="ARCHIVE_AND_LOCAL_VARIATION_ONLY")
    payload = encode(science)
    require(sha(payload) == science_lock, "ARCHIVE_REPLAY_DISAGREES")
    publish("science.json", payload)
    receipt.update(status="ARCHIVE_AUDIT_COMPLETE", science_sha256=sha(payload),
                   diagnostics=diagnostics, mechanism_cards=1, new_physical_survivors=0)
except Exception as exc:
    receipt.update(status="HOLD", error=f"{type(exc).__name__}: {exc}")
finally:
    receipt.update(wall_s=time.perf_counter()-wall, cpu_s=time.process_time()-cpu)
    publish("receipt.json", encode(receipt))
    print("F0_RUN=" + str(run))
    print(json.dumps(receipt, indent=2))
sys.exit(0 if receipt["status"] == "ARCHIVE_AUDIT_COMPLETE" else 1)
