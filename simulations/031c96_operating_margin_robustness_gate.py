from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

QBALL_SOURCE = SIM / "031b2a_global_qball_activated_scalar_control.py"
TRANSLATION_SOURCE = SIM / "031b2b0_qball_payload_adjacent_translation_gate.py"
QBALL_SUMMARY = DATA / "031b2a_global_qball_activated_scalar_control_summary.json"
D96_SUMMARY = DATA / "031b2d96_combined_coupled_linear_goldstone_summary.json"

OUT_JSON = DATA / "031c96_operating_margin_robustness_summary.json"
OUT_CSV = DATA / "031c96_operating_margin_threshold_scan.csv"
DOMAIN_CSV = DATA / "031c96_domain_reconstruction_scan.csv"
PERTURB_CSV = DATA / "031c96_parameter_geometry_robustness_scan.csv"

EXPECTED_QBALL_SHA = "67e5d1196fde8e3e6f72eda34f15bb3dec2b8a17ebbd7ee8e13107c63e2560f5"
EXPECTED_TRANSLATION_SHA = "84bac7f59b44adbc6763923e5dfa184476ab31e02cacba271b525392f2f824cc"

G0 = 9.80665
SOURCE_RADIUS_M = 0.95
PAYLOAD_OVERLAP_LIMIT = 1.0e-10
NOMINAL_LEAK_LIMIT = 1.0e-4
NOMINAL_BACK_LIMIT = 1.0e-2
INTERIOR_LEAK_LIMIT = 8.0e-5
INTERIOR_BACK_LIMIT = 8.0e-3
ALPHA_MAX = 100.0

DOMAIN_MU_R_VALUES = (0.8, 3.0, 5.0)
LEAK_CAPS = (1.0e-4, 8.0e-5, 5.0e-5, 1.0e-5, 1.0e-6)
BACK_CAPS = (1.0e-2, 8.0e-3, 5.0e-3, 2.5e-3)

DEFAULT_PAYLOAD_RADIUS = 0.10
DEFAULT_PAYLOAD_CENTER = 2.05

GEOMETRY_CASES = (
    ("nominal", 0.10, 2.05),
    ("radius_minus10pct", 0.09, 2.05),
    ("radius_plus10pct", 0.11, 2.05),
    ("center_minus5cm", 0.10, 2.00),
    ("center_plus5cm", 0.10, 2.10),
    ("adverse_large_close", 0.11, 2.00),
    ("benign_small_far", 0.09, 2.10),
)

PARAMETER_PERTURBATIONS = (
    ("omega_minus", "omega", -0.005),
    ("omega_plus", "omega", +0.005),
    ("epsilon_minus2pct", "epsilon_scale", 0.98),
    ("epsilon_plus2pct", "epsilon_scale", 1.02),
    ("chi_minus2pct", "chi_scale", 0.98),
    ("chi_plus2pct", "chi_scale", 1.02),
)


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Missing required file: {path}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def to_builtin(value: Any):
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {str(k): to_builtin(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_builtin(v) for v in value]
    return value


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def relative_spread(values: list[float]) -> float:
    if not values:
        return math.inf
    mean = float(np.mean(values))
    return (max(values) - min(values)) / max(abs(mean), 1.0e-300)


def fraction_inside_sphere(shell_radius, center_distance, sphere_radius):
    r = np.asarray(shell_radius, dtype=float)
    d = float(center_distance)
    R = float(sphere_radius)

    if abs(d) <= 1.0e-15:
        return (r <= R).astype(float)

    denom = 2.0 * r * d
    c = np.divide(
        R**2 - r**2 - d**2,
        denom,
        out=np.full_like(r, np.inf),
        where=denom != 0.0,
    )
    fraction = np.clip(0.5 * (c + 1.0), 0.0, 1.0)
    zero = r <= 1.0e-15
    fraction[zero] = 1.0 if d <= R else 0.0
    return fraction


def fraction_inside_payload(shell_radius, payload_distance, payload_radius):
    r = np.asarray(shell_radius, dtype=float)
    d = float(payload_distance)
    R = float(payload_radius)
    denom = 2.0 * r * d
    c = np.divide(
        r**2 + d**2 - R**2,
        denom,
        out=np.full_like(r, np.inf),
        where=denom != 0.0,
    )
    fraction = np.clip(0.5 * (1.0 - c), 0.0, 1.0)
    zero = r <= 1.0e-15
    fraction[zero] = 1.0 if d <= R else 0.0
    return fraction


def source_weight_shells(qmod, case, omega):
    x = np.asarray(case["x"], dtype=float)
    y, yp, u, _ = case["solution"].sol(x)
    A = np.exp(np.clip(-0.5 * u**2, -700.0, 0.0))
    potential = qmod.W(y)

    source_on = 0.5 * yp**2 + 0.5 * omega**2 * y**2 + A * potential
    source_off = 0.5 * yp**2 + 0.5 * omega**2 * y**2 + potential
    noether = omega * y**2

    common = 4.0 * math.pi * x**2
    return {
        "on_energy": common * source_on,
        "off_energy": common * source_off,
        "noether": common * noether,
    }


def containment_all(
    case,
    shells,
    shift,
    payload_radius=DEFAULT_PAYLOAD_RADIUS,
    payload_center=DEFAULT_PAYLOAD_CENTER,
):
    x = np.asarray(case["x"], dtype=float)
    radii = np.asarray(case["physical_radius"], dtype=float)

    source_fraction = fraction_inside_sphere(
        radii,
        float(shift),
        SOURCE_RADIUS_M,
    )

    payload_distance = float(payload_center) - float(shift)
    payload_fraction = fraction_inside_payload(
        radii,
        payload_distance,
        payload_radius,
    )

    leak = {}
    overlap = {}

    for name, shell in shells.items():
        total = float(np.trapezoid(shell, x))
        leak[name] = float(
            np.trapezoid(shell * (1.0 - source_fraction), x)
            / max(total, 1.0e-300)
        )
        overlap[name] = float(
            np.trapezoid(shell * payload_fraction, x)
            / max(total, 1.0e-300)
        )

    return {
        "leak": leak,
        "overlap": overlap,
        "conservative_leak": max(leak.values()),
        "conservative_overlap": max(overlap.values()),
    }


def max_shift_for_names(
    case,
    shells,
    leak_limit,
    names,
    payload_radius=DEFAULT_PAYLOAD_RADIUS,
    payload_center=DEFAULT_PAYLOAD_CENTER,
):
    def violation(shift):
        metrics = containment_all(
            case,
            shells,
            shift,
            payload_radius,
            payload_center,
        )
        leak_ratio = max(metrics["leak"][n] for n in names) / leak_limit
        overlap_ratio = (
            max(metrics["overlap"][n] for n in names)
            / PAYLOAD_OVERLAP_LIMIT
        )
        return max(leak_ratio, overlap_ratio) - 1.0

    shifts = np.linspace(0.0, 0.94, 377)
    values = np.asarray([violation(float(s)) for s in shifts])
    allowed = np.where(values <= 0.0)[0]

    if len(allowed) == 0:
        return None

    idx = int(allowed[-1])
    if idx >= len(shifts) - 1:
        return float(shifts[idx])

    lo = float(shifts[idx])
    hi = float(shifts[idx + 1])

    if values[idx] <= 0.0 and values[idx + 1] > 0.0:
        return float(
            brentq(
                violation,
                lo,
                hi,
                xtol=1.0e-10,
                rtol=1.0e-11,
                maxiter=120,
            )
        )

    return lo


def force_at_geometry(
    tmod,
    qmod,
    case,
    shift,
    alpha,
    payload_radius,
    payload_center,
    surface_points=None,
    radial_points=None,
    angular_points=None,
):
    old = (
        tmod.PAYLOAD_RADIUS_M,
        tmod.PAYLOAD_CENTER_M,
        tmod.SURFACE_MU_POINTS,
        tmod.CM_RADIAL_POINTS,
        tmod.CM_ANGULAR_POINTS,
    )

    tmod.PAYLOAD_RADIUS_M = float(payload_radius)
    tmod.PAYLOAD_CENTER_M = float(payload_center)

    if surface_points is not None:
        tmod.SURFACE_MU_POINTS = int(surface_points)
    if radial_points is not None:
        tmod.CM_RADIAL_POINTS = int(radial_points)
    if angular_points is not None:
        tmod.CM_ANGULAR_POINTS = int(angular_points)

    try:
        return tmod.force_solution(qmod, case, float(shift), float(alpha))
    finally:
        (
            tmod.PAYLOAD_RADIUS_M,
            tmod.PAYLOAD_CENTER_M,
            tmod.SURFACE_MU_POINTS,
            tmod.CM_RADIAL_POINTS,
            tmod.CM_ANGULAR_POINTS,
        ) = old


def alpha_for_backreaction_cap(
    tmod,
    qmod,
    case,
    shift,
    cap,
    alpha_hint,
    payload_radius=DEFAULT_PAYLOAD_RADIUS,
    payload_center=DEFAULT_PAYLOAD_CENTER,
    surface_points=None,
    radial_points=None,
    angular_points=None,
):
    cache = {}

    def evaluate(alpha):
        key = round(float(alpha), 12)
        if key not in cache:
            cache[key] = force_at_geometry(
                tmod,
                qmod,
                case,
                shift,
                alpha,
                payload_radius,
                payload_center,
                surface_points,
                radial_points,
                angular_points,
            )
        return cache[key]

    candidates = sorted(
        set(
            [float(alpha_hint)]
            + list(np.geomspace(5.0, ALPHA_MAX, 34))
            + [10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 50.0, 75.0, 100.0]
        )
    )

    valid = []
    for alpha in candidates:
        result = evaluate(alpha)
        if result is not None and math.isfinite(result["backreaction"]):
            valid.append((alpha, result))

    feasible = [
        (alpha, result)
        for alpha, result in valid
        if result["backreaction"] <= cap
    ]

    if not feasible:
        return None

    low_alpha, low_result = max(feasible, key=lambda item: item[0])
    above = [
        (alpha, result)
        for alpha, result in valid
        if alpha > low_alpha and result["backreaction"] > cap
    ]

    if not above:
        return low_result

    high_alpha, _ = min(above, key=lambda item: item[0])

    def root_function(alpha):
        result = evaluate(alpha)
        if result is None:
            raise RuntimeError("force_solution failed inside alpha bracket")
        return result["backreaction"] - cap

    alpha_root = float(
        brentq(
            root_function,
            low_alpha,
            high_alpha,
            xtol=2.0e-8,
            rtol=2.0e-10,
            maxiter=100,
        )
    )
    return evaluate(alpha_root)


def build_case(qmod, tmod, omega, epsilon, chi, mediator_range, mu_r):
    qmod.X_MATCH = float(mu_r) / float(epsilon)
    row = {
        "omega": float(omega),
        "epsilon": float(epsilon),
        "chi": float(chi),
        "chi_factor": math.nan,
        "E_inventory_J": math.nan,
    }
    return tmod.reconstruct(qmod, row, mediator_range)


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def operating_point(
    tmod,
    qmod,
    case,
    shells,
    leak_cap,
    back_cap,
    alpha_hint,
    names=("on_energy", "off_energy", "noether"),
    payload_radius=DEFAULT_PAYLOAD_RADIUS,
    payload_center=DEFAULT_PAYLOAD_CENTER,
    surface_points=None,
    radial_points=None,
    angular_points=None,
):
    shift = max_shift_for_names(
        case,
        shells,
        leak_cap,
        names,
        payload_radius,
        payload_center,
    )
    if shift is None:
        return None

    containment = containment_all(
        case,
        shells,
        shift,
        payload_radius,
        payload_center,
    )

    force = alpha_for_backreaction_cap(
        tmod,
        qmod,
        case,
        shift,
        back_cap,
        alpha_hint,
        payload_radius,
        payload_center,
        surface_points,
        radial_points,
        angular_points,
    )

    if force is None:
        return None

    return {
        "shift_m": float(shift),
        "alpha_m": float(force["alpha_m"]),
        "energy_J": float(force["E_inventory_J"]),
        "backreaction": float(force["backreaction"]),
        "surface_min_mps2": float(force["surface_min_mps2"]),
        "surface_max_mps2": float(force["surface_max_mps2"]),
        "a_cm_mps2": float(force["a_cm_mps2"]),
        "conservative_leak": float(containment["conservative_leak"]),
        "conservative_overlap": float(containment["conservative_overlap"]),
        "leak_on_energy": float(containment["leak"]["on_energy"]),
        "leak_off_energy": float(containment["leak"]["off_energy"]),
        "leak_noether": float(containment["leak"]["noether"]),
        "overlap_on_energy": float(containment["overlap"]["on_energy"]),
        "overlap_off_energy": float(containment["overlap"]["off_energy"]),
        "overlap_noether": float(containment["overlap"]["noether"]),
    }


def point_pass(point, leak_cap, back_cap):
    return bool(
        point is not None
        and point["conservative_leak"] <= leak_cap * (1.0 + 2.0e-6)
        and point["conservative_overlap"] <= PAYLOAD_OVERLAP_LIMIT
        and point["backreaction"] <= back_cap * (1.0 + 2.0e-6)
        and point["surface_min_mps2"] >= G0 * (1.0 - 2.0e-8)
        and point["a_cm_mps2"] > G0
        and math.isfinite(point["energy_J"])
        and point["energy_J"] > 0.0
    )


def main():
    print("=== 031C96 OPERATING-MARGIN ROBUSTNESS GATE ===")
    print("CLAIM_CLASS=STABLE_96GJ_INTRINSIC_SOURCE_OPERATING_POINT_MARGIN_AND_THRESHOLD_CERTIFICATION")
    print("NEW_OPERATOR=NO")
    print("SOURCE_THEORY_RETUNED_FOR_PRIMARY_RESULT=NO")
    print("OPERATING_ALPHA_AND_TRANSLATION_REOPTIMIZED_WITHIN_DECLARED_GATES=YES")
    print("ACTIVATION_OFFSTATE_CLOSED=NO")
    print("FULL_METRIC_BACKREACTION_CLOSED=NO")
    print("NONLINEAR_FRAGMENTATION_CLOSED=NO")
    print("PRACTICAL_DEVICE=NO")

    for path in (QBALL_SOURCE, TRANSLATION_SOURCE, QBALL_SUMMARY, D96_SUMMARY):
        require(path)

    q_sha = sha256(QBALL_SOURCE)
    t_sha = sha256(TRANSLATION_SOURCE)
    print(f"QBALL_SOURCE_SHA256={q_sha}")
    print(f"TRANSLATION_SOURCE_SHA256={t_sha}")

    provenance_source_pass = bool(
        q_sha == EXPECTED_QBALL_SHA
        and t_sha == EXPECTED_TRANSLATION_SHA
    )
    print(f"SOURCE_PROVENANCE_PASS={provenance_source_pass}")

    qmod = load_module("c96_qball", QBALL_SOURCE)
    tmod = load_module("c96_translation", TRANSLATION_SOURCE)

    qsummary = json.loads(QBALL_SUMMARY.read_text())
    d96 = json.loads(D96_SUMMARY.read_text())

    intrinsic_green = str(d96.get("classification", "")).startswith("GREEN_96GJ_INTRINSIC_QBALL")
    print(f"D96_INTRINSIC_STABILITY_GREEN={intrinsic_green}")

    candidate = d96["candidate"]
    omega = float(candidate["omega"])
    epsilon = float(candidate["epsilon"])
    chi = float(candidate["chi"])
    stored_energy = float(candidate["operating_energy_J"])
    stored_shift = float(candidate["operating_shift_m"])
    stored_alpha = float(candidate["operating_alpha_m"])
    stored_leak = float(candidate["operating_source_leak"])
    stored_back = float(candidate["operating_backreaction"])

    mediator_range = float(qsummary["mediator_range_m"])

    print(f"OMEGA={omega:.15e}")
    print(f"EPSILON={epsilon:.15e}")
    print(f"CHI={chi:.15e}")
    print(f"STORED_OPERATING_ENERGY_J={stored_energy:.15e}")
    print(f"STORED_SHIFT_M={stored_shift:.15e}")
    print(f"STORED_ALPHA_M={stored_alpha:.15e}")
    print(f"STORED_SOURCE_LEAK={stored_leak:.15e}")
    print(f"STORED_BACKREACTION={stored_back:.15e}")
    print(f"MEDIATOR_RANGE_M={mediator_range:.15e}")

    # ------------------------------------------------------------------
    # A. Independent reproduction on the original 0.8 Compton-length BVP.
    # ------------------------------------------------------------------
    print("\n=== STAGE A: ORIGINAL OPERATING-POINT REPRODUCTION + TAIL DEFINITIONS ===")
    case_short = build_case(qmod, tmod, omega, epsilon, chi, mediator_range, 0.8)
    if case_short is None:
        raise RuntimeError("Failed to reconstruct original D96 source")

    shells_short = source_weight_shells(qmod, case_short, omega)
    independent_containment = containment_all(case_short, shells_short, stored_shift)
    legacy_leak, legacy_overlap = tmod.containment(case_short, stored_shift)
    stored_force = force_at_geometry(
        tmod, qmod, case_short, stored_shift, stored_alpha,
        DEFAULT_PAYLOAD_RADIUS, DEFAULT_PAYLOAD_CENTER,
    )
    if stored_force is None:
        raise RuntimeError("Stored D96 operating point did not reproduce force root")

    baseline_energy_rel = relerr(stored_force["E_inventory_J"], stored_energy)
    baseline_back_rel = relerr(stored_force["backreaction"], stored_back)
    baseline_leak_rel = relerr(legacy_leak, stored_leak)
    independent_leak_rel = relerr(legacy_leak, independent_containment["leak"]["on_energy"])

    baseline_reproduction_pass = bool(
        baseline_energy_rel <= 8.0e-4
        and baseline_back_rel <= 8.0e-4
        and baseline_leak_rel <= 8.0e-4
        and independent_leak_rel <= 2.0e-8
        and stored_force["surface_min_mps2"] >= G0 * (1.0 - 2.0e-8)
    )

    original_all_tail_defs_pass = bool(
        independent_containment["conservative_leak"] <= NOMINAL_LEAK_LIMIT * (1.0 + 2.0e-6)
        and independent_containment["conservative_overlap"] <= PAYLOAD_OVERLAP_LIMIT
    )

    print(
        f"BASELINE E={stored_force['E_inventory_J']:.15e} "
        f"E_RELERR={baseline_energy_rel:.6e} "
        f"BACK={stored_force['backreaction']:.15e} "
        f"BACK_RELERR={baseline_back_rel:.6e} "
        f"LEGACY_LEAK={legacy_leak:.15e} "
        f"INDEPENDENT_ON_LEAK={independent_containment['leak']['on_energy']:.15e} "
        f"OFF_LEAK={independent_containment['leak']['off_energy']:.15e} "
        f"NOETHER_LEAK={independent_containment['leak']['noether']:.15e} "
        f"CONSERVATIVE_LEAK={independent_containment['conservative_leak']:.15e}"
    )
    print(f"BASELINE_REPRODUCTION_PASS={baseline_reproduction_pass}")
    print(f"ORIGINAL_POINT_ALL_TAIL_DEFINITIONS_PASS={original_all_tail_defs_pass}")

    # ------------------------------------------------------------------
    # B. Reconstruct the same source on larger scalar domains.
    # ------------------------------------------------------------------
    print("\n=== STAGE B: LONG-DOMAIN OPERATING RECONSTRUCTION ===")
    domain_rows = []
    cases = {}

    for mu_r in DOMAIN_MU_R_VALUES:
        case = case_short if math.isclose(mu_r, 0.8) else build_case(
            qmod, tmod, omega, epsilon, chi, mediator_range, mu_r
        )
        if case is None:
            domain_rows.append({"mu_r": mu_r, "success": False})
            print(f"DOMAIN MU_R={mu_r:.3f} SUCCESS=False")
            continue

        cases[mu_r] = case
        shells = source_weight_shells(qmod, case, omega)
        cont = containment_all(case, shells, stored_shift)
        force = force_at_geometry(
            tmod, qmod, case, stored_shift, stored_alpha,
            DEFAULT_PAYLOAD_RADIUS, DEFAULT_PAYLOAD_CENTER,
        )

        row = {
            "mu_r": mu_r,
            "x_match": float(qmod.X_MATCH),
            "success": force is not None,
            "energy_J": math.nan if force is None else force["E_inventory_J"],
            "backreaction": math.nan if force is None else force["backreaction"],
            "a_cm_mps2": math.nan if force is None else force["a_cm_mps2"],
            "surface_min_mps2": math.nan if force is None else force["surface_min_mps2"],
            "conservative_leak": cont["conservative_leak"],
            "on_leak": cont["leak"]["on_energy"],
            "off_leak": cont["leak"]["off_energy"],
            "noether_leak": cont["leak"]["noether"],
        }
        domain_rows.append(row)
        print(
            f"DOMAIN MU_R={mu_r:.3f} X_MATCH={row['x_match']:.6f} "
            f"E_J={row['energy_J']:.15e} BACK={row['backreaction']:.9e} "
            f"A_CM={row['a_cm_mps2']:.9e} CONS_LEAK={row['conservative_leak']:.9e}"
        )

    successful_domains = [r for r in domain_rows if r.get("success")]
    domain_energy_spread = relative_spread([float(r["energy_J"]) for r in successful_domains])
    domain_back_spread = relative_spread([float(r["backreaction"]) for r in successful_domains])
    domain_acm_spread = relative_spread([float(r["a_cm_mps2"]) for r in successful_domains])
    domain_leak_abs_spread = (
        max(float(r["conservative_leak"]) for r in successful_domains)
        - min(float(r["conservative_leak"]) for r in successful_domains)
        if successful_domains else math.inf
    )

    domain_reconstruction_pass = bool(
        len(successful_domains) == len(DOMAIN_MU_R_VALUES)
        and domain_energy_spread < 1.0e-2
        and domain_back_spread < 1.0e-2
        and domain_acm_spread < 1.0e-2
        and domain_leak_abs_spread < 1.0e-5
    )
    print(f"DOMAIN_ENERGY_REL_SPREAD={domain_energy_spread:.9e}")
    print(f"DOMAIN_BACKREACTION_REL_SPREAD={domain_back_spread:.9e}")
    print(f"DOMAIN_A_CM_REL_SPREAD={domain_acm_spread:.9e}")
    print(f"DOMAIN_LEAK_ABS_SPREAD={domain_leak_abs_spread:.9e}")
    print(f"DOMAIN_RECONSTRUCTION_PASS={domain_reconstruction_pass}")

    # Use the longest-domain reconstruction for all remaining operating tests.
    case_ref = cases.get(5.0)
    if case_ref is None:
        raise RuntimeError("Longest-domain reference reconstruction unavailable")
    shells_ref = source_weight_shells(qmod, case_ref, omega)

    # ------------------------------------------------------------------
    # C. Definition sensitivity at the original declared thresholds.
    # ------------------------------------------------------------------
    print("\n=== STAGE C: SOURCE-TAIL DEFINITION SENSITIVITY ===")
    definition_rows = []
    for name in ("on_energy", "off_energy", "noether"):
        point = operating_point(
            tmod, qmod, case_ref, shells_ref,
            NOMINAL_LEAK_LIMIT, NOMINAL_BACK_LIMIT, stored_alpha,
            names=(name,),
        )
        row = {
            "scan_type": "tail_definition",
            "tail_definition": name,
            "leak_cap": NOMINAL_LEAK_LIMIT,
            "back_cap": NOMINAL_BACK_LIMIT,
            "success": point is not None,
        }
        if point:
            row.update(point)
        definition_rows.append(row)
        if point:
            print(
                f"TAIL_DEF={name} SHIFT={point['shift_m']:.9e} "
                f"ALPHA={point['alpha_m']:.9e} E_J={point['energy_J']:.15e} "
                f"CONS_LEAK={point['conservative_leak']:.9e} BACK={point['backreaction']:.9e}"
            )
        else:
            print(f"TAIL_DEF={name} SUCCESS=False")

    # ------------------------------------------------------------------
    # D. Conservative threshold Pareto map: max of all three tail measures.
    # ------------------------------------------------------------------
    print("\n=== STAGE D: CONSERVATIVE LEAK/BACKREACTION THRESHOLD MAP ===")
    threshold_rows = []
    points_by_caps = {}

    for leak_cap in LEAK_CAPS:
        shift = max_shift_for_names(
            case_ref, shells_ref, leak_cap,
            ("on_energy", "off_energy", "noether"),
        )
        if shift is None:
            for back_cap in BACK_CAPS:
                threshold_rows.append({
                    "scan_type": "threshold",
                    "leak_cap": leak_cap,
                    "back_cap": back_cap,
                    "success": False,
                })
            continue

        cont = containment_all(case_ref, shells_ref, shift)
        for back_cap in BACK_CAPS:
            force = alpha_for_backreaction_cap(
                tmod, qmod, case_ref, shift, back_cap, stored_alpha,
            )
            point = None
            if force is not None:
                point = {
                    "shift_m": shift,
                    "alpha_m": force["alpha_m"],
                    "energy_J": force["E_inventory_J"],
                    "backreaction": force["backreaction"],
                    "surface_min_mps2": force["surface_min_mps2"],
                    "surface_max_mps2": force["surface_max_mps2"],
                    "a_cm_mps2": force["a_cm_mps2"],
                    "conservative_leak": cont["conservative_leak"],
                    "conservative_overlap": cont["conservative_overlap"],
                    "leak_on_energy": cont["leak"]["on_energy"],
                    "leak_off_energy": cont["leak"]["off_energy"],
                    "leak_noether": cont["leak"]["noether"],
                }

            row = {
                "scan_type": "threshold",
                "leak_cap": leak_cap,
                "back_cap": back_cap,
                "success": point is not None,
            }
            if point:
                row.update(point)
                points_by_caps[(leak_cap, back_cap)] = point
            threshold_rows.append(row)

            if point:
                print(
                    f"THRESH LEAK_CAP={leak_cap:.3e} BACK_CAP={back_cap:.3e} "
                    f"SHIFT={point['shift_m']:.9e} ALPHA={point['alpha_m']:.9e} "
                    f"E_GJ={point['energy_J']/1e9:.9f} "
                    f"LEAK={point['conservative_leak']:.9e} "
                    f"BACK={point['backreaction']:.9e} A_CM={point['a_cm_mps2']:.9e}"
                )
            else:
                print(f"THRESH LEAK_CAP={leak_cap:.3e} BACK_CAP={back_cap:.3e} SUCCESS=False")

    interior = points_by_caps.get((INTERIOR_LEAK_LIMIT, INTERIOR_BACK_LIMIT))
    interior_pass = point_pass(interior, INTERIOR_LEAK_LIMIT, INTERIOR_BACK_LIMIT)
    print(f"INTERIOR_20PCT_MARGIN_POINT_PASS={interior_pass}")
    if interior:
        print(f"INTERIOR_20PCT_MARGIN_ENERGY_J={interior['energy_J']:.15e}")
        print(f"INTERIOR_20PCT_MARGIN_ENERGY_GJ={interior['energy_J']/1e9:.12f}")
        print(f"INTERIOR_20PCT_MARGIN_SHIFT_M={interior['shift_m']:.15e}")
        print(f"INTERIOR_20PCT_MARGIN_ALPHA_M={interior['alpha_m']:.15e}")

    # ------------------------------------------------------------------
    # E. Finite-payload geometry robustness at the interior operating caps.
    # ------------------------------------------------------------------
    print("\n=== STAGE E: FINITE-PAYLOAD GEOMETRY ROBUSTNESS ===")
    geometry_rows = []
    geometry_passes = []

    for label, radius, center in GEOMETRY_CASES:
        point = operating_point(
            tmod, qmod, case_ref, shells_ref,
            INTERIOR_LEAK_LIMIT, INTERIOR_BACK_LIMIT, stored_alpha,
            names=("on_energy", "off_energy", "noether"),
            payload_radius=radius,
            payload_center=center,
        )
        passed = point_pass(point, INTERIOR_LEAK_LIMIT, INTERIOR_BACK_LIMIT)
        geometry_passes.append(passed)
        row = {
            "scan_type": "geometry",
            "label": label,
            "payload_radius_m": radius,
            "payload_center_m": center,
            "success": point is not None,
            "pass": passed,
        }
        if point:
            row.update(point)
        geometry_rows.append(row)
        if point:
            print(
                f"GEOM={label} R={radius:.6f} CENTER={center:.6f} "
                f"E_GJ={point['energy_J']/1e9:.9f} SHIFT={point['shift_m']:.9e} "
                f"ALPHA={point['alpha_m']:.9e} A_CM={point['a_cm_mps2']:.9e} PASS={passed}"
            )
        else:
            print(f"GEOM={label} SUCCESS=False PASS=False")

    geometry_robustness_pass = bool(all(geometry_passes))
    print(f"FINITE_PAYLOAD_GEOMETRY_ROBUSTNESS_PASS={geometry_robustness_pass}")

    # ------------------------------------------------------------------
    # F. High-order payload quadrature reconstruction at the interior point.
    # ------------------------------------------------------------------
    print("\n=== STAGE F: PAYLOAD QUADRATURE RECONSTRUCTION ===")
    quadrature_pass = False
    high_quad = None
    quad_metrics = {}

    if interior is not None:
        high_quad = force_at_geometry(
            tmod, qmod, case_ref,
            interior["shift_m"], interior["alpha_m"],
            DEFAULT_PAYLOAD_RADIUS, DEFAULT_PAYLOAD_CENTER,
            surface_points=361,
            radial_points=24,
            angular_points=32,
        )

        if high_quad is not None:
            quad_metrics = {
                "energy_relerr": relerr(high_quad["E_inventory_J"], interior["energy_J"]),
                "backreaction_relerr": relerr(high_quad["backreaction"], interior["backreaction"]),
                "a_cm_relerr": relerr(high_quad["a_cm_mps2"], interior["a_cm_mps2"]),
                "surface_min_relerr": relerr(high_quad["surface_min_mps2"], interior["surface_min_mps2"]),
            }
            quadrature_pass = bool(
                max(quad_metrics.values()) <= 2.0e-3
                and high_quad["surface_min_mps2"] >= G0 * (1.0 - 2.0e-8)
            )

    print(f"HIGH_QUADRATURE_METRICS={json.dumps(to_builtin(quad_metrics), sort_keys=True)}")
    print(f"PAYLOAD_QUADRATURE_RECONSTRUCTION_PASS={quadrature_pass}")

    # ------------------------------------------------------------------
    # G. Local source-parameter perturbations. Diagnostic only; no retuning
    #    is allowed to improve the nominal result.
    # ------------------------------------------------------------------
    print("\n=== STAGE G: LOCAL SOURCE-PARAMETER SURVIVAL ===")
    perturb_rows = []
    perturb_passes = []

    for label, kind, value in PARAMETER_PERTURBATIONS:
        o2 = omega
        e2 = epsilon
        c2 = chi
        if kind == "omega":
            o2 = omega + value
        elif kind == "epsilon_scale":
            e2 = epsilon * value
        elif kind == "chi_scale":
            c2 = chi * value
        else:
            raise RuntimeError(f"Unknown perturbation kind: {kind}")

        case2 = build_case(qmod, tmod, o2, e2, c2, mediator_range, 5.0)
        point = None
        if case2 is not None:
            shells2 = source_weight_shells(qmod, case2, o2)
            point = operating_point(
                tmod, qmod, case2, shells2,
                INTERIOR_LEAK_LIMIT, INTERIOR_BACK_LIMIT, stored_alpha,
                names=("on_energy", "off_energy", "noether"),
            )

        passed = point_pass(point, INTERIOR_LEAK_LIMIT, INTERIOR_BACK_LIMIT)
        perturb_passes.append(passed)
        row = {
            "scan_type": "parameter_perturbation",
            "label": label,
            "omega": o2,
            "epsilon": e2,
            "chi": c2,
            "success": point is not None,
            "pass": passed,
        }
        if point:
            row.update(point)
        perturb_rows.append(row)

        if point:
            print(
                f"PERTURB={label} OMEGA={o2:.9e} EPS={e2:.9e} CHI={c2:.9e} "
                f"E_GJ={point['energy_J']/1e9:.9f} SHIFT={point['shift_m']:.9e} "
                f"ALPHA={point['alpha_m']:.9e} PASS={passed}"
            )
        else:
            print(f"PERTURB={label} SUCCESS=False PASS=False")

    local_parameter_survival_pass = bool(all(perturb_passes))
    print(f"LOCAL_PARAMETER_SURVIVAL_PASS={local_parameter_survival_pass}")

    # ------------------------------------------------------------------
    # Decision ledger.
    # ------------------------------------------------------------------
    print("\n=== FINAL 031C96 DECISION ===")

    edge_margin_certified = bool(
        baseline_reproduction_pass
        and original_all_tail_defs_pass
        and stored_leak < 0.95 * NOMINAL_LEAK_LIMIT
        and stored_back < 0.95 * NOMINAL_BACK_LIMIT
    )

    family_robust = bool(
        provenance_source_pass
        and intrinsic_green
        and baseline_reproduction_pass
        and domain_reconstruction_pass
        and interior_pass
        and geometry_robustness_pass
        and quadrature_pass
        and local_parameter_survival_pass
    )

    if not provenance_source_pass or not intrinsic_green or not baseline_reproduction_pass:
        classification = "RED_D96_OPERATING_ROBUSTNESS_PROVENANCE_OR_BASELINE_REPRODUCTION_FAILURE"
        next_step = "REPAIR_PROVENANCE_OR_REPRODUCTION_BEFORE_PHYSICS_PROMOTION"
    elif family_robust:
        classification = (
            "GREEN_96GJ_STABLE_SOURCE_FAMILY_HAS_INTERIOR_OPERATING_SURVIVOR_"
            "EXACT_96P141GJ_EDGE_QUOTE_NOT_MARGIN_CERTIFIED"
        )
        next_step = "031D_ACTIVATION_OFFSTATE_COMPLETE_GATE_CONTROL_ENERGY_AND_RECIPROCITY"
    else:
        classification = "YELLOW_96GJ_INTRINSIC_SOURCE_STABLE_BUT_OPERATING_MARGIN_ROBUSTNESS_NOT_CLOSED"
        next_step = "INSPECT_ONLY_FAILED_031C96_ROBUSTNESS_SUBGATE_BEFORE_031D"

    print(f"SOURCE_PROVENANCE_PASS={provenance_source_pass}")
    print(f"D96_INTRINSIC_STABILITY_GREEN={intrinsic_green}")
    print(f"BASELINE_REPRODUCTION_PASS={baseline_reproduction_pass}")
    print(f"ORIGINAL_POINT_ALL_TAIL_DEFINITIONS_PASS={original_all_tail_defs_pass}")
    print(f"EXACT_96P141_EDGE_MARGIN_CERTIFIED={edge_margin_certified}")
    print(f"DOMAIN_RECONSTRUCTION_PASS={domain_reconstruction_pass}")
    print(f"INTERIOR_20PCT_MARGIN_POINT_PASS={interior_pass}")
    print(f"FINITE_PAYLOAD_GEOMETRY_ROBUSTNESS_PASS={geometry_robustness_pass}")
    print(f"PAYLOAD_QUADRATURE_RECONSTRUCTION_PASS={quadrature_pass}")
    print(f"LOCAL_PARAMETER_SURVIVAL_PASS={local_parameter_survival_pass}")
    print(f"031C96_CLASSIFICATION={classification}")
    print(f"NEXT={next_step}")
    print("NONLINEAR_FRAGMENTATION_CLOSED=NO")
    print("ACTIVATION_OFFSTATE_CLOSED=NO")
    print("FULL_METRIC_BACKREACTION_CLOSED=NO")
    print("RADIATIVE_NATURALNESS_CLOSED=NO")
    print("EMPIRICAL_FIFTH_FORCE_CLOSURE=NO")
    print("PRACTICAL_DEVICE=NO")

    all_threshold_rows = definition_rows + threshold_rows
    all_perturb_rows = geometry_rows + perturb_rows
    write_csv(OUT_CSV, all_threshold_rows)
    write_csv(DOMAIN_CSV, domain_rows)
    write_csv(PERTURB_CSV, all_perturb_rows)

    output = {
        "claim_class": "STABLE_96GJ_INTRINSIC_SOURCE_OPERATING_POINT_MARGIN_AND_THRESHOLD_CERTIFICATION",
        "candidate": candidate,
        "source_provenance_pass": provenance_source_pass,
        "intrinsic_stability_green": intrinsic_green,
        "baseline": {
            "reproduction_pass": baseline_reproduction_pass,
            "energy_relerr": baseline_energy_rel,
            "backreaction_relerr": baseline_back_rel,
            "legacy_leak_relerr": baseline_leak_rel,
            "independent_on_leak_relerr": independent_leak_rel,
            "tail_definitions_at_original_shift": independent_containment,
            "original_point_all_tail_definitions_pass": original_all_tail_defs_pass,
            "exact_96p141_edge_margin_certified": edge_margin_certified,
        },
        "domain_reconstruction": {
            "rows": domain_rows,
            "energy_relative_spread": domain_energy_spread,
            "backreaction_relative_spread": domain_back_spread,
            "a_cm_relative_spread": domain_acm_spread,
            "leak_absolute_spread": domain_leak_abs_spread,
            "pass": domain_reconstruction_pass,
        },
        "tail_definition_scan": definition_rows,
        "threshold_scan": threshold_rows,
        "interior_20pct_margin_point": interior,
        "interior_20pct_margin_pass": interior_pass,
        "geometry_scan": geometry_rows,
        "geometry_robustness_pass": geometry_robustness_pass,
        "quadrature": {
            "high_order_result": high_quad,
            "relative_errors": quad_metrics,
            "pass": quadrature_pass,
        },
        "parameter_perturbations": perturb_rows,
        "local_parameter_survival_pass": local_parameter_survival_pass,
        "family_operating_robustness_green": family_robust,
        "classification": classification,
        "next": next_step,
        "claim_limits": [
            "The intrinsic isolated Q-ball l=0..8 coupled-linear spectrum is inherited from the GREEN D96 gate.",
            "The exact 96.141-GJ point is an edge optimum at the original leak/backreaction ceilings and is not called margin-certified here unless it has explicit headroom.",
            "The primary robust operating test uses 20% tighter leak and payload-backreaction caps and the maximum of on-energy, off-energy, and Noether X-tail definitions.",
            "Small omega/epsilon/chi perturbations are robustness diagnostics only and are not used to optimize the nominal result.",
            "Finite-amplitude fragmentation/fission remains open.",
            "Activation/off-state and its gate/control energy remain open.",
            "Full physical-metric backreaction remains open.",
            "Radiative naturalness and empirical fifth-force/EP/PPN closure remain open.",
            "No practical device or experimental new force is established.",
        ],
    }

    OUT_JSON.write_text(json.dumps(to_builtin(output), indent=2, sort_keys=True) + "\n")
    print(f"SUMMARY_JSON={OUT_JSON.resolve()}")
    print(f"THRESHOLD_CSV={OUT_CSV.resolve()}")
    print(f"DOMAIN_CSV={DOMAIN_CSV.resolve()}")
    print(f"PERTURB_CSV={PERTURB_CSV.resolve()}")


if __name__ == "__main__":
    main()
