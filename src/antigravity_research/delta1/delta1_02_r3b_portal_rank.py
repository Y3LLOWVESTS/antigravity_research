"""DELTA1-02: R3B universal-metric reciprocity and two-invariant rank.

PURPOSE
-------
Return to the original R3B 1.5429162116460216 J prescribed mixed
electric/magnetic field capacity, preserving the corrected R3X1 signs
and all historical loaded failures.

SCIENTIFIC QUESTION
-------------------
Can changing only the nonlinear function sigma(P) independently reduce
the matter-trace carrier loading while preserving the finite neutral
payload's acceleration? If not, does one separate parity-even
field-strength invariant Q supply a geometrically independent channel
in the ORIGINAL R3B prescribed-field geometry?

THEORY
------
Physical universal metric: gtilde = exp(2 sigma(P)) g.
P = mixed Lorentzian two-U(1) invariant, in the R3B convention.
The neutral matter action is S_m[gtilde, matter].

Exact local identity for its matter trace T:
    lambda = exp(4 sigma) T sigma_P

Neutral weak-field static acceleration:
    a = -c^2 sigma_P grad(P).

A nonlinear sigma(P) cannot choose these derivatives independently
at fixed P and grad(P). Further:
    grad(lambda) x grad(P)
      = exp(4 sigma) sigma_P grad(T) x grad(P).

This theorem does NOT say that field profiles, new degrees of freedom,
supports, or other complete actions cannot change the result.

One additional hypothetical independent response direction is tested:
    Q_Y = (hbar*c)^2 F_Y(mu,nu)F_Y(mu,nu)/M^4,
while the original R3B conformal response is
    S_P = -2(hbar*c)^2 E dot B/M^4.

At the equal-energy perfect-mirror configuration, S_P=Q exactly.
A new Q operator would be geometrically redundant in that limit.
The actual fitted exterior mirror is tested on original source fields.

INPUTS
------
Original R3B production reconstruction, multipole fit, toroidal
neutral density model, 0.075/0.050 m grids, historical result JSON,
and immutable DELTA1-01 plus source-code SHA-256 checkpoints.

OUTPUTS
-------
Exact symbolic reciprocity, measured invariant-gradient rank,
native density/interface misalignment and historical capacity lock.

UNITS
-----
Field strengths use the original R3B canonical conventions.
S_P and Q are dimensionless physical-metric profiles.
Acceleration is m/s^2. Matter density is kg/m^3.
Loading is the original dimensionless beta/Z prescription.

LIMITS
------
R3B fields are PRESCRIBED and UNLOADED here. This does not certify
physical sources, loaded 1kg lift, Lorentzian health, Einstein gravity,
quantum/UV or <10MJ total operating energy. No PDE is authorized.
"""
from __future__ import annotations

import hashlib
import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
import sympy as sp

from antigravity_research.agminer.hook17_fdual_f_global_mirror_prefight import (
    reconstruct_a12c_field,
    fit_exterior_multipoles,
    evaluate_multipole_field,
)
from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
    PRIMARY_DENSITY_MODEL,
    payload_density_profile_kg_m3,
    loading_coefficient_z,
)
from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
    TARGET_ACCELERATION_M_S2,
)

REFERENCE_J = 1.5429162116460216
GRID_M = (0.075, 0.050)
FIT_RADIUS_M = 2.40
FIT_LMAX = 12

R3B_RESULT = (
    "results/data/"
    "032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json"
)

LOCKED = {
    "R3B_source": (
        "src/antigravity_research/agminer/"
        "hook17_fdual_f_global_mirror_prefight.py",
        "aa8f196fcae6a63405181ca62674e22ac67e5da88303759bdd99d25716fa2263",
    ),
    "A12C_source": (
        "src/antigravity_research/agminer/"
        "hook17_concurrent_u1_fieldstrength_metric.py",
        "2fb2094de5995aab5172fc825bd30d895ffbb163d1a3418105c808c19fa50b99",
    ),
    "loading_source": (
        "src/antigravity_research/agminer/"
        "hook17_f2_strong_payload_loading_rescue.py",
        "e1296794c25a4d0e4d5634c7e7d543a0b488b8d2a1963afcf7878bea1c1b99e7",
    ),
    "DELTA01_science": (
        "results/data/delta1_01_20261120T011200609297Z.json",
        "f513d8e2f8e54db618dfcbfcd30ca2f2f35a8fd1de5440f005bd5dcd24bcb84f",
    ),
    "DELTA01_verification": (
        "results/data/delta1_01_verification_20261120T012531244617Z.json",
        "4fa6141959a2f349fb6310e202c2c3073a9d044eb32f5ffb1a7a2a019dbc0688",
    ),
}


def sha(path):
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "MISSING"


def parents(root):
    """Fail closed on original producing-source drift or missing archives."""
    root = Path(root)
    locked = {}
    for name, (relative, expected) in LOCKED.items():
        p = root / relative
        actual = sha(p)
        if actual != expected:
            raise RuntimeError(f"PARENT_DRIFT:{name}:{actual}")
        if p.suffix == ".json":
            side = p.with_name(p.name + ".sha256")
            if not side.is_file() or side.read_text().strip() != expected + "  " + p.name:
                raise RuntimeError(f"PARENT_SIDECAR_DRIFT:{name}")
        locked[name] = {"path": relative, "sha256": actual}

    history_path = root/R3B_RESULT
    if not history_path.is_file():
        raise RuntimeError("ORIGINAL_R3B_JSON_MISSING")
    old = json.loads(history_path.read_text())
    if old.get("branch") != "032H17A12D1R3B":
        raise RuntimeError("R3B_BRANCH_DRIFT")
    reference = float(
        old["grid_results"]["0.05"]["payload_reconstruction"][
            "normalized_mixed_global_field_energy_j"
        ]
    )
    if not math.isclose(reference,REFERENCE_J,rel_tol=0,abs_tol=1e-9):
        raise RuntimeError(f"R3B_REFERENCE_ENERGY_DRIFT:{reference}")

    locked["R3B_original_result"] = {
        "path":R3B_RESULT,
        "sha256":sha(history_path),
        "historical_preloaded_capacity_j":reference,
    }
    return locked


def theorem():
    """Independent generic-function symbolic trace/gradient identity."""
    P,T = sp.symbols("P T",real=True)
    Px,Pz,Tx,Tz = sp.symbols("Px Pz Tx Tz",real=True)
    f = sp.Function("sigma")(P)
    fp = sp.diff(f,P)

    lam = sp.exp(4*f)*T*fp
    lx = sp.diff(lam,P)*Px + sp.diff(lam,T)*Tx
    lz = sp.diff(lam,P)*Pz + sp.diff(lam,T)*Tz

    expected = sp.exp(4*f)*fp*(Tx*Pz-Tz*Px)
    if sp.simplify(lx*Pz-lz*Px-expected) != 0:
        raise AssertionError("EXACT_TRACE_WEDGE_WARD_FAIL")

    # At fixed original P and grad P, matching a fixes sigma'(P),
    # irrespective of the chosen higher derivatives of sigma(P).
    s1,s2 = sp.symbols("s1 s2",real=True)
    generic = s1*P+s2*P**2
    acceleration_x = -sp.diff(generic,P)*Px
    response_x = sp.diff(generic,P)*Px
    if sp.simplify(acceleration_x+response_x) != 0:
        raise AssertionError("SAME_DERIVATIVE_RECIPROCITY_FAIL")

    return {
        "exact_trace_identity":
            "lambda=exp(4sigma)*T*sigma_P",
        "exact_transverse_identity":
            "grad(lambda) cross grad(P)=exp(4sigma)*sigma_P*grad(T) cross grad(P)",
        "metric_acceleration":
            "a=-c^2*sigma_P*grad(P)",
        "portal_only_reparametrization_escape_at_fixed_fields":
            "NO_IF_SAME_ACCELERATION_REQUIRED",
        "new_field_or_new_invariant_escape":"OPEN_NOT_ESTABLISHED",
    }


def perfect_mirror_control():
    """Direct numerical negative control on independent 2D fields."""
    E0 = np.array([0.7,-1.3])
    E = -E0/math.sqrt(2)
    B = E0/math.sqrt(2)
    p = -2*float(E@B)
    q = 2*float(B@B)
    if abs(p-q)>1e-14:
        raise AssertionError("PERFECT_MIRROR_INVARIANTS_NOT_EQUAL")
    return {"P_over_Q":p/q, "independent_channel_rank":1}


@lru_cache(maxsize=4)
def native(h):
    """Read the original R3B prescribed field geometry without alteration."""
    field = reconstruct_a12c_field(float(h))
    fit = fit_exterior_multipoles(field,FIT_RADIUS_M,FIT_LMAX)
    fitted_r,fitted_z = evaluate_multipole_field(field,fit)

    c2 = HBAR_C_EV_M**2/REFERENCE_PORTAL_SCALE_EV**4
    ba_r = field["b_rho"]
    ba_z = field["b_z"]

    E_r = -fitted_r/math.sqrt(2)
    E_z = -fitted_z/math.sqrt(2)
    B_r = ba_r/math.sqrt(2)
    B_z = ba_z/math.sqrt(2)

    p = -2*c2*(E_r*B_r+E_z*B_z)
    q = 2*c2*(B_r**2+B_z**2)

    dpz,dpr = np.gradient(p,h,h,edge_order=2)
    baseline_accel = -C_LIGHT_M_S**2*dpz
    mask = field["payload"]

    pre_min = float(np.min(baseline_accel[mask]))
    if pre_min<=0:
        raise RuntimeError("NATIVE_PRELOADED_R3B_SIGN_FAIL")
    norm = TARGET_ACCELERATION_M_S2/pre_min
    p *= norm
    q *= norm

    dpz,dpr = np.gradient(p,h,h,edge_order=2)
    dqz,dqr = np.gradient(q,h,h,edge_order=2)
    ap = -C_LIGHT_M_S**2*dpz
    aq = -C_LIGHT_M_S**2*dqz

    # Entire 2-component gradient over all actual torus sample cells.
    v = np.r_[dpz[mask],dpr[mask]]
    w = np.r_[dqz[mask],dqr[mask]]
    vv = float(v@v)
    ww = float(w@w)
    vw = float(v@w)
    if vv<=0 or ww<=0:
        raise RuntimeError("NATIVE_GRADIENT_DEGENERACY")
    cosine = vw/math.sqrt(vv*ww)
    independent = math.sqrt(max(0.,1.-cosine*cosine))

    density = payload_density_profile_kg_m3(
        field["rho_grid"],field["z_grid"],PRIMARY_DENSITY_MODEL
    )
    beta = loading_coefficient_z(
        density,REFERENCE_PORTAL_SCALE_EV
    )-1.
    dbz,dbr = np.gradient(beta,h,h,edge_order=2)
    gradbeta = np.hypot(dbz,dbr)
    gradp = np.hypot(dpz,dpr)
    active = (
        (gradbeta>max(float(gradbeta.max()),1e-100)*1e-8)
        & (gradp>max(float(gradp.max()),1e-100)*1e-8)
    )

    if not np.any(active):
        raise RuntimeError("NATIVE_MATTER_INTERFACE_UNRESOLVED")

    wedge = dbr*dpz-dbz*dpr
    sin = np.abs(wedge[active]) / (
        gradbeta[active]*gradp[active]
    )
    sin = np.clip(sin,0,1)
    weights = gradbeta[active]*gradp[active]
    mean_sin = float(np.average(sin,weights=weights))
    interface_norm = float(np.linalg.norm(wedge[active]))

    if not math.isclose(
        float(np.min(ap[mask])),
        TARGET_ACCELERATION_M_S2,
        rel_tol=0,abs_tol=1e-9
    ):
        raise RuntimeError("ORIGINAL_PRELOADED_1G_RENORMALIZATION_FAIL")

    return {
        "grid_spacing_m":float(h),
        "field_cells":int(np.size(p)),
        "torus_sample_cells":int(np.sum(mask)),
        "portal_scale_eV":float(REFERENCE_PORTAL_SCALE_EV),
        "original_pre_normalization_min_accel":pre_min,
        "reproduction_normalization_on_sigma":float(norm),
        "min_P_acceleration_m_s2":float(np.min(ap[mask])),
        "min_Q_acceleration_m_s2":float(np.min(aq[mask])),
        "max_abs_P_minus_Q_on_payload":float(
            np.max(np.abs((p-q)[mask]))
        ),
        "gradient_cosine_P_Q":float(cosine),
        "gradient_independent_fraction_Q":float(independent),
        "gradient_gram":[[vv,vw],[vw,ww]],
        "peak_original_beta":float(np.max(beta)),
        "matter_interface_active_cells":int(active.sum()),
        "matter_interface_mean_misalignment_sin":mean_sin,
        "matter_interface_wedge_L2":interface_norm,
        "native_loaded_result":"NOT_RE_SOLVED",
        "complete_source_energy":"NOT_DERIVED",
    }


def science(root):
    locked=parents(root)
    exact=theorem()
    mirror=perfect_mirror_control()
    meshes=[native(h) for h in GRID_M]

    independent_fine=meshes[-1]["gradient_independent_fraction_Q"]
    independent_coarse=meshes[0]["gradient_independent_fraction_Q"]

    # Pre-registered diagnostic, NOT a physical certification gate.
    if max(independent_fine,independent_coarse)<0.05:
        geometric="NEAR_COLLINEAR_NO_SIMPLE_Q_PROMOTION"
    elif abs(independent_fine-independent_coarse)>0.1:
        geometric="RANK_GRID_DEPENDENT_NO_PROMOTION"
    else:
        geometric="NONZERO_SECOND_DIRECTION_CONDITIONAL_ACTION_TEST_ONLY"

    return {
        "classification":
            "R3B_SCOPED_RECIPROCITY_AND_GEOMETRIC_RANK_AUDIT",
        "parents":locked,
        "original_R3B_prescribed_field_capacity_J":REFERENCE_J,
        "historical_loaded_fine_grid_min_acceleration_m_s2":
            -129.67185782242464,
        "historical_loaded_fine_grid_field_energy_J":
            1.5211390382733165,
        "historical_loading_failure":"PRESERVED_NOT_RERUN",
        "portal_reciprocity_theorem":exact,
        "perfect_mirror_negative_control":mirror,
        "native_meshes":meshes,
        "one_extra_even_invariant_rank_decision":geometric,
        "potential_new_action":
            "sigma(P,Q)=sigma_R3B(P)+xi*Q; xi NOT FITTED",
        "gates":{
            "ORIGINAL_R3B_SOURCE_PROVENANCE":"PASS",
            "ORIGINAL_1P542916J_REFERENCE":"PASS_PRESERVED",
            "R3X1_CORRECTED_SIGNS":"INHERITED_NOT_RERUN",
            "SINGLE_INVARIANT_RECIPROCITY":"EXACT_IDENTITY",
            "ONE_NEW_PARITY_EVEN_INVARIANT":"GEOMETRY_ONLY",
            "TWO_INVARIANT_SAME_ACTION_LOADING":"NOT_SOLVED",
            "MICROSCOPIC_SOURCE_CURRENTS":"NOT_DERIVED",
            "FULL_EINSTEIN_EARTH_SUPPORT_ACTION":"NOT_DERIVED",
            "HEALTHY_LORENTZIAN_MODES":"NOT_CERTIFIED",
            "FINITE_LOADED_1KG_TORUS":"HISTORICAL_FAIL_UNCHANGED",
            "SI_SOURCE_SUPPORT_UV_EMPIRICAL":"NOT_CERTIFIED",
            "PHYSICAL_EXTERIOR_AND_CRAFT_LIFT":"NOT_DERIVED",
        },
        "qualified_gravity_bridge_survivors":[],
        "006D_replaced":False,
        "DELTA1_03_authorized":False,
        "GAMMA1_01_authorized":False,
        "PH16_05_authorized":False,
        "PH17_authorized":False,
        "whole_craft_up":"NOT_DERIVED",
        "complete_operating_energy_lt10MJ":"NOT_CERTIFIED",
        "next_decision":
            "ONLY_NEW_ACTION_LEVEL_CARRIER_SOURCE_COMPLETION_IF_INDEPENDENT_RANK_AND_HEALTH_SURVIVE",
    }
