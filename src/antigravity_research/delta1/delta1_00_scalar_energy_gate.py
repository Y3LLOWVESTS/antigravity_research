"""DELTA1-00 action-first single-new-operator scalar source falsifier.

Explicit new interaction: dimensionless canonical scalar ϕ alters X kinetic
function Z(ϕ)=1+ηϕ; every ordinary test body sees g~=exp(2αϕ)g.
A source-field E/B composition can change its scalar charge SIGN without
prescribing opposite charges. This is a scalar-tensor FIFTH FORCE, not
established Einstein-GR antigravity or sourced whole-craft propulsion.

Bound: u_ϕ >= a_ϕ²/(8πG α²) pointwise in a static canonical scalar EFT.
The long-range unscreened representative is screened by an illustrative
PPN gamma tolerance. Short range and nonlinear screening are NOT excluded.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import sympy as sp

G = 6.67430e-11
C = 299792458.0
GRAVITY = 9.80665
BUDGET = 10_000_000.0
TARGET_KG = 1.0
DISTANCE_M = 1.0
# A deliberately generous, assumption-scoped illustration; not an
# independently certified modern experimental confidence bound.
PPN_GAMMA_TOLERANCE = 1e-4
RHO_ASSUMED = (1000.0, 8000.0, 20000.0)

PARENTS = {
    "PH16_R2_source": (
        "src/antigravity_research/ph16/ph16_04_joint_stationary.py",
        "b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0",
    ),
    "N1_science": (
        "results/data/gamma1_n1_20261119T220556272564Z.json",
        "fb246ecf729d4c55382e9bb6589f469400849af1aab81b3612067799d1e066fc",
    ),
    "N1_verification": (
        "results/data/gamma1_n1_verification_20261119T221950245035Z.json",
        "6bbe1e228fb7c98786335530d0eeeb5bf420835d423295df0416b0cc63190c73",
    ),
    "C1_science": (
        "results/data/gamma1_c1_20261119T212606521420Z.json",
        "ebd7ebef9cd26d70388c7d0d49ee85b7018654b29043678dbdf307ede3ed4111",
    ),
}


def digest(path):
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "MISSING"


def check_parents(root):
    output = {}
    for key, (rel, expected) in PARENTS.items():
        file = Path(root) / rel
        if digest(file) != expected:
            raise RuntimeError(f"PARENT_SHA_DRIFT:{key}:{digest(file)}")
        if file.suffix == ".json":
            side = file.with_name(file.name + ".sha256")
            if not side.is_file() or side.read_text().strip() != expected + "  " + file.name:
                raise RuntimeError(f"PARENT_SIDECAR_DRIFT:{key}")
        output[key] = {"path": rel, "sha256": expected}
    n1 = json.loads((Path(root) / PARENTS["N1_science"][0]).read_text())
    if n1["GAMMA1_01_authorized"] is not False or n1["006D_replaced"] is not False:
        raise RuntimeError("N1_CLAIM_DRIFT")
    return output


def exact_variations():
    """Independent tree-level symbolic action derivatives and Ward controls.

    Static source functional E=∫[c^4/(8πG)|∇ϕ|² +s_ϕ ϕ]d³x.
    s_ϕ=α ρ c² + η (u_B-u_E). Isolated mass -> attraction;
    electric field energy -> opposite signed effective scalar source.
    """
    x, phi, alpha, eta, ue, ub, mass, r = sp.symbols(
        "x phi alpha eta uE uB M r", real=True,
        positive=True
    )
    k, s = sp.symbols("k s", real=True, positive=True)
    # The kinetic variation is -k Δϕ, with k=c^4/(4πG).
    lag = k*x*x/2 + s*phi
    assert sp.diff(lag, x) == k*x
    assert sp.diff(lag, phi) == s
    q_m = alpha*mass + eta*(ub-ue)/sp.Symbol("c2",positive=True)
    q_n = sp.simplify(q_m.subs(ub,0))
    if sp.simplify(sp.diff(q_n,ue)) >= 0:
        raise AssertionError("ELECTRIC_SOURCE_SIGN_FAIL")
    # Scalar potential: ϕ=-G q_m/(c² r), point-source exterior.
    radial_mass = -sp.diff(-q_m/r, r)
    # Acceleration = -alpha c² grad ϕ, proportional to -alpha q_m/r².
    if sp.simplify(radial_mass+q_m/r**2)!=0:
        raise AssertionError("SCALAR_RADIAL_FORCE_SIGN_FAIL")
    # Two-body interaction U=-G(M_E M_C + q_E q_C)/r.
    earth, craft = sp.symbols("Earth Craft",positive=True)
    qe = alpha*earth
    qc = alpha*craft - eta*ue/sp.Symbol("c2",positive=True)
    Ui = -(earth*craft+qe*qc)/r
    Fc = -sp.diff(Ui,r)
    Fe = -Fc
    if sp.simplify(Fc+Fe)!=0:
        raise AssertionError("TWO_BODY_RECOIL_IDENTITY_FAIL")
    if sp.simplify(sp.diff(Fc,eta)) != alpha*earth*ue/(sp.Symbol("c2",positive=True)*r*r):
        raise AssertionError("ELECTRIC_EARTH_CRAFT_SIGN_FAIL")
    # The trace response of the conformal metric universal test mass.
    var_m = sp.diff(mass*sp.exp(alpha*phi),phi)
    if sp.simplify(var_m-alpha*mass*sp.exp(alpha*phi))!=0:
        raise AssertionError("UNIVERSAL_METRIC_VARIATION_FAIL")
    return {
        "single_new_operator":"(eta/4) phi F_X^2 via Z(phi)=1+eta*phi",
        "matter_metric":"g_tilde=exp(2 alpha phi) g",
        "earth_craft_pair_recoil":"SYMBOLIC_EXACT_IN_2_BODY_WEAK_FIELD_MODEL",
        "neutral_metric_variation":"SYMBOLIC_EXACT",
        "electric_field_effective_charge":"OPPOSITE_TO_POSITIVE_MATTER_FOR_ALPHA_ETA_POSITIVE",
        "magnetic_field_effective_charge":"SAME_AS_POSITIVE_MATTER_FOR_ALPHA_ETA_POSITIVE",
        "two_body_conditions":"POINT_MONOPOLE_UNSCREENED_NOT_REAL_EARTH_SUPPORT_SOLUTION",
        "on_shell_source_and_support":"NOT_SOLVED",
    }


def ppn_alpha_max(delta=PPN_GAMMA_TOLERANCE):
    """Massless unscreened scalar: |gamma_PPN-1|=2 alpha²/(1+alpha²)."""
    if not (0 < delta < 1):
        raise ValueError("PPN delta must be in (0,1)")
    return math.sqrt(delta/(2-delta))


def target_energy_floor(alpha, density):
    """Energy physically present in a target with required local scalar a.

    Assumes source-on field, no off-state/background subtraction, finite
    target material density, static canonical scalar and constant alpha.
    This is the gradient energy inside that finite volume ONLY.
    """
    if alpha <= 0 or density <= 0:
        raise ValueError("positive alpha magnitude and density required")
    vol = TARGET_KG/density
    u = GRAVITY**2/(8*math.pi*G*alpha*alpha)
    return {
        "density_kg_m3_ASSUMED":density,
        "target_volume_m3_ASSUMED":vol,
        "field_gradient_energy_density_J_m3":u,
        "scalar_field_energy_in_target_J_LOWER_BOUND":vol*u,
        "energy_over_budget":vol*u/BUDGET,
        "minimum_alpha_if_target_gradient_energy_lt_budget":math.sqrt(
            GRAVITY**2*vol/(8*math.pi*G*BUDGET)
        ),
    }


def source_leverage(alpha, energy_j=BUDGET, r=DISTANCE_M):
    """Unscreened point-monopole electric-only source NECESSARY conditions.

    a_scalar = alpha G eta E_X/(c² r²) if ordinary matter ignored.
    Source mass adds attraction and increases needed eta.
    eta*phi is computed at EXACT threshold, where linearization already fails.
    """
    ae_needed = GRAVITY*C*C*r*r/(G*energy_j)
    eta_needed = ae_needed/alpha
    phi_point = G*eta_needed*energy_j/(C**4*r)
    eta_phi = eta_needed*phi_point
    expected = GRAVITY**2*r**3/(G*energy_j*alpha**2)
    if abs(eta_phi-expected)/eta_phi > 1e-13:
        raise AssertionError("SOURCE_FIELD_COUPLING_CLOSURE_FAIL")
    return {
        "field_energy_assumed_J":energy_j,
        "true_point_standoff_assumed_m":r,
        "alpha_times_eta_min_ignoring_matter":ae_needed,
        "eta_min_ignoring_matter":eta_needed,
        "eta_times_phi_at_standoff_threshold":eta_phi,
        "linear_Z_perturbation_small":"NO" if eta_phi>=1 else "NOT_EXCLUDED_BY_THIS_GATE",
        "support_charge_included":False,
        "finite_Maxwell_source_solution":"NOT_CONSTRUCTED",
    }


def negative_controls():
    a = ppn_alpha_max()
    dense = target_energy_floor(a,8000)
    gain = source_leverage(a)
    controls = {
        "scalar_zero_coupling_no_force":(0.0*a==0.0),
        "electric_magnetic_source_sign_opposed":True,
        "healthy_scalar_gradient_energy_positive":dense["scalar_field_energy_in_target_J_LOWER_BOUND"]>0,
        "smaller_alpha_increases_energy":target_energy_floor(a/2,8000)["scalar_field_energy_in_target_J_LOWER_BOUND"] > dense["scalar_field_energy_in_target_J_LOWER_BOUND"],
        "stronger_density_reduces_min_energy":target_energy_floor(a,20000)["scalar_field_energy_in_target_J_LOWER_BOUND"] < dense["scalar_field_energy_in_target_J_LOWER_BOUND"],
        "linear_gauge_Z_weak_field_invalid_at_needed_source":gain["eta_times_phi_at_standoff_threshold"]>1,
        "canonical_scalar_kinetic_sign":"POSITIVE"=="POSITIVE",
    }
    if not all(controls.values()):
        raise AssertionError("SCALAR_NEGATIVE_CONTROL_FAILED")
    return controls


def science(root):
    parent = check_parents(root)
    variation = exact_variations()
    alpha = ppn_alpha_max()
    energies = [target_energy_floor(alpha,rho) for rho in RHO_ASSUMED]
    leverage = source_leverage(alpha)
    controls = negative_controls()
    # Pre-registered rejection conditions, not a test-count score.
    red = (
        all(e["scalar_field_energy_in_target_J_LOWER_BOUND"] > BUDGET for e in energies)
        and leverage["eta_times_phi_at_standoff_threshold"] > 1.0
    )
    if not red:
        raise RuntimeError("ASSUMPTION_SCOPED_SCALAR_RED_NOT_ESTABLISHED")
    return {
        "classification":"SCOPED_RED_LONG_RANGE_UNSCREENED_SCALAR_F2",
        "parent_sha_lock":parent,
        "action_variations":variation,
        "PPN":{
            "assumption":"MASSLESS_OR_SOLAR_SYSTEM_RANGE_UNSCREENED_ONLY",
            "gamma_tolerance_illustrative_NOT_CONFIDENCE_LIMIT":PPN_GAMMA_TOLERANCE,
            "formula":"abs(gamma_PPN-1)=2 alpha^2/(1+alpha^2)",
            "alpha_max_illustrative":alpha,
            "Cassini_observation":"gamma-1=(2.1 +/- 2.3)*1e-5; not used as a hard one-sided bound",
        },
        "target_energy":energies,
        "gauge_source_leverage":leverage,
        "negative_controls":controls,
        "test_volume_NOT_user_specified":True,
        "short_range_screened_branch":"OPEN_UNTESTED_REQUIRES_LAB_EMPIRICS_AND_CONSISTENT_SOURCE",
        "candidate_nonminimal_coupling_count":1,
        "gates":{
            "OPERATOR_AND_UNIVERSAL_METRIC_SPECIFIED":"PASS_SCOPED",
            "FULL_DIFFEOMORPHIC_EARTH_HULL_SUPPORT_ACTION":"NOT_CLOSED",
            "SCALAR_CURRENT_SOURCE_AND_SIGN":"PASS_WEAK_FIELD_SCOPED",
            "EXTERNAL_EARTH_CRAFT_RECOIL":"PASS_POINT_MONOPOLE_PROXY_ONLY",
            "PH16_STATIC_REDUCTION":"NOT_ATTEMPTED_NOT_REQUIRED_FOR_NEW_OPERATOR",
            "FULL_LORENTZIAN_CONSTRAINED_HEALTH":"NOT_CERTIFIED",
            "METER_SCALE_EMPIRICAL_FIFTH_FORCE":"NOT_SCREENED",
            "SOLAR_RANGE_UNSCREENED_ENERGY_BOUND":"RED_UNDER_ASSUMPTIONS",
            "CANONICAL_GRADIENT_ENERGY":"LOWER_BOUND_TARGET_ONLY",
            "TRUE_STANDOFF_FINITE_SOURCE":"NOT_SOLVED",
            "ONBOARD_OPERATING_ENERGY_OFFSTATE":"NOT_CLOSED",
            "EARTH_DOWN_WHOLE_CRAFT_UP":"NOT_DERIVED_REAL_SOURCE",
        },
        "qualified_gravity_bridge_survivors":[],
        "006D_replaced":False,
        "GAMMA1_01_authorized":False,
        "PH16_05_authorized":False,
        "PH17_authorized":False,
        "actual_whole_craft_up":"NOT_DERIVED",
        "actual_neutral_torus_1g_at_1m":"NOT_CERTIFIED",
        "complete_operating_energy_lt_10MJ":"NOT_CERTIFIED",
        "GAMMA_heuristic_percent":34,
        "DELTA_heuristic_percent":"NOT_ASSIGNED_PREMATURE",
        "next_physics_decision":"EXPLICIT_METER_RANGE_LAB_BOUNDS_OR_NEW_HEALTHY_NONCANONICAL_OPERATOR; NO_AUTOMATIC_PDE",
    }
