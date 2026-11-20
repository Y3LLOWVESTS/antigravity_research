"""GAMMA1-C1: finite-scope high-information source-to-gravity decision atlas.

New questions: differential Y Euler vs local constitutive variation (D0 erratum),
weak-field GR DEC source cost, minimal healthy universal scalar exchange sign,
conditional conformal neutral geometry. No fully sourced Einstein, real Earth,
whole-craft force, operating-energy certificate, or new physics is claimed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import numpy as np
import sympy as sp

G_SI = 6.67430e-11
C_SI = 299792458.0
A_TARGET = 9.80665
D_TARGET = 1.0
ENERGY_CEILING = 10_000_000.0

PARENTS = {
    "PH16_R2_source": (
        "src/antigravity_research/ph16/ph16_04_joint_stationary.py",
        "b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0",
    ),
    "R11_science": (
        "results/data/gamma1_00r11_20261119T074039011670Z.json",
        "ac7050c648959ee0daa21bed994d8cdc34abb261d08433f302d4362af163acef",
    ),
    "R11_archive": (
        "results/data/gamma1_00r11_20261119T074039011670Z_Noether_Schur_12_L12.npz",
        "d5d0de1f5614be104d28c4fe51b157cb1f26815b905a14495791e7a049fa46fd",
    ),
    "R12_science": (
        "results/data/gamma1_00r12_20261119T201141220587Z.json",
        "7ebddf22bd718dc9729b1d63cb72943d75e379c12ce68420399edaafcf99bad6",
    ),
    "R12_verification": (
        "results/data/gamma1_00r12_verification_20261119T202521821183Z.json",
        "583ffee14d177af47628d2759a5b61a124f7ec968e83de7cad430b4575860b92",
    ),
    "D0_science": (
        "results/data/gamma1_d0_20261119T205007375929Z.json",
        "a89998f3a3ab7721295ecbf568795d417e2ec9769fd059caf7e0b6446e380a80",
    ),
    "D0_verification": (
        "results/data/gamma1_d0_verification_20261119T210423530904Z.json",
        "8f7281eef967c3e8b0612d25c5427b14aa8473b8185f3f0ca93063500a87b230",
    ),
}


def sha(path):
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "MISSING"


def check_parents(root):
    output = {}
    for name, (rel, expected) in PARENTS.items():
        p = Path(root) / rel
        got = sha(p)
        if got != expected:
            raise RuntimeError(f"PARENT_SHA_DRIFT:{name}:{got}")
        if p.suffix in (".json", ".npz"):
            side = p.with_name(p.name + ".sha256")
            if not side.is_file() or side.read_text().strip() != expected + "  " + p.name:
                raise RuntimeError(f"PARENT_SIDECAR_DRIFT:{name}")
        output[name] = {"path": rel, "sha256": got}

    d0 = json.loads((Path(root) / PARENTS["D0_science"][0]).read_text())
    r12 = json.loads((Path(root) / PARENTS["R12_science"][0]).read_text())
    if d0.get("GAMMA1_01_authorized") is not False or r12.get("GAMMA1_01_authorized") is not False:
        raise RuntimeError("PARENT_AUTHORIZATION_DRIFT")
    if d0.get("classification") != "SCOPED_LOCAL_PROXY_ACTION_WARDS_PASS_PHYSICAL_BRIDGE_NOT_ESTABLISHED":
        raise RuntimeError("D0_CLASSIFICATION_DRIFT")
    if r12.get("r11_fixed_N", {}).get("rank") != 2:
        raise RuntimeError("R11_RANK_TWO_HISTORY_DRIFT")
    return output


def manufacture(x, *, p_amp=0.6, k=0.08, scale2=8.0):
    """Exterior vacuum X dipole with manufactured OFF-SHELL lambda."""
    x = np.asarray(x, float)
    r2 = float(x @ x)
    r = np.sqrt(r2)
    if r < .6:
        raise ValueError("restrict to dipole exterior, r>=0.6")
    potential = p_amp * x[2] / r**3
    grad_phi = p_amp * (
        np.array([0., 0., 1.]) / r**3 - 3 * x[2] * x / r**5
    )
    amp = k * np.exp(-r2 / scale2)
    lam = .025 + amp * x[0] * x[1]
    grad_lam = amp * np.array([
        x[1] * (1 - 2*x[0]**2/scale2),
        x[0] * (1 - 2*x[1]**2/scale2),
        -2*x[0]*x[1]*x[2]/scale2,
    ])
    return potential, grad_phi, lam, grad_lam


def d0_euler_amendment():
    """Y Euler bulk current, not D0's local constitutive derivative.

    At F_Y=0, J_Y^i=(grad lambda cross grad A_X0)^i in our orientation.
    The matter-trace lambda is manufactured, not an on-shell solution.
    """
    x = np.array([1.2, .75, 1.4])
    pot, grad_phi, lam, grad_lam = manufacture(x)
    exact = np.cross(grad_lam, grad_phi)
    if np.linalg.norm(exact) < 1e-5:
        raise AssertionError("DEGENERATE_MANUFACTURED_Y_SOURCE")

    errors = []
    for h in (.08, .04, .02, .01):
        gphi = np.zeros(3)
        glam = np.zeros(3)
        for i in range(3):
            e = np.zeros(3)
            e[i] = h
            plus = manufacture(x+e)
            minus = manufacture(x-e)
            gphi[i] = (plus[0]-minus[0])/(2*h)
            glam[i] = (plus[2]-minus[2])/(2*h)
        errors.append(float(np.linalg.norm(np.cross(glam, gphi)-exact)))

    if not (errors[0] > errors[1] > errors[2] > errors[3] and errors[-1] < 1e-5):
        raise AssertionError("DIFFERENTIAL_Y_NONCONVERGENCE:" + str(errors))

    # Independent 4D epsilon contraction, orientation [0123]=+1.
    from itertools import permutations
    eps4 = np.zeros((4,4,4,4), int)
    for ix in permutations(range(4)):
        eps4[ix] = (-1)**sum(
            ix[i] > ix[j] for i in range(4) for j in range(i+1,4)
        )
    FX = np.zeros((4,4))
    FX[0,1:] = -grad_phi
    FX[1:,0] = grad_phi
    dl = np.r_[0.,grad_lam]
    j4 = .5*np.einsum("m,mnrs,rs->n", dl, eps4, FX)

    if abs(j4[0]) > 1e-14 or np.linalg.norm(j4[1:]-exact) > 1e-14:
        raise AssertionError("4D_HODGE_VS_3D_Y_EULER_SIGN_FAIL")

    aligned = np.cross(2*.7*pot*grad_phi,grad_phi)
    if np.linalg.norm(aligned) > 1e-14:
        raise AssertionError("LAMBDA_OF_A0_NULL_FAIL")
    if not np.allclose(-exact,np.cross(grad_lam,-grad_phi),rtol=1e-14,atol=1e-14):
        raise AssertionError("X_ORIENTATION_REVERSAL_FAIL")

    return {
        "manufactured_potential":float(pot),
        "manufactured_lambda":float(lam),
        "manufactured_Y_source_norm":float(np.linalg.norm(exact)),
        "differential_source_vector":exact.tolist(),
        "centered_difference_steps":[.08,.04,.02,.01],
        "centered_difference_errors":errors,
        "constant_lambda_bulk_source":"EXACT_ZERO_BY_BIANCHI",
        "lambda_equals_function_of_A0_source":"EXACT_ZERO_STATIC_ELECTRIC",
        "X_polarity_reversal":"ODD",
        "physical_on_shell_source":"NOT_SOLVED",
    }


def exact_bianchi():
    """Vacuum dipole harmonic identity and divergence-free Euler current."""
    x,y,z = sp.symbols("x y z", real=True)
    phi = z/(x*x+y*y+z*z)**sp.Rational(3,2)
    lap = sp.factor(sum(sp.diff(phi,v,2) for v in (x,y,z)))
    if lap != 0:
        raise AssertionError("DIPOLE_NOT_VACUUM_HARMONIC")

    lam = x*y*sp.exp(-(x*x+y*y+z*z)/8)
    gL = [sp.diff(lam,v) for v in (x,y,z)]
    gP = [sp.diff(phi,v) for v in (x,y,z)]
    j = [
        gL[1]*gP[2]-gL[2]*gP[1],
        gL[2]*gP[0]-gL[0]*gP[2],
        gL[0]*gP[1]-gL[1]*gP[0],
    ]
    divergence = sp.factor(sum(
        sp.diff(j[i],v) for i,v in enumerate((x,y,z))
    ))
    if divergence != 0:
        raise AssertionError("MANUFACTURED_CURRENT_NOT_CONSERVED")
    return {
        "vacuum_dipole_laplacian":"ZERO_EXACT",
        "Y_current_divergence":"ZERO_EXACT",
        "constant_lambda_no_bulk_source":"ZERO_EXACT",
    }


def gr_dec_bound():
    """Static linearized GR, type-I DEC, minimum source-target distance d.

    DEC yields |epsilon + p1+p2+p3| <= 4 epsilon.
    Therefore |a| <= 4 G E_total / (c^2 d^2).
    This energy INCLUDES positive source rest/support stress-energy
    and cannot silently be equated with the operating-energy budget.
    """
    Emin = A_TARGET*C_SI**2*D_TARGET**2/(4*G_SI)
    Amax = 4*G_SI*ENERGY_CEILING/(C_SI**2*D_TARGET**2)
    if not (Emin>1e27 and Amax<1e-18):
        raise AssertionError("GR_COST_BOUND_NUMERICAL_DRIFT")
    extremizers = {
        "all_positive":4.0,
        "all_negative":-2.0,
        "zero":1.0,
    }
    return {
        "assumptions":[
            "linearized_GR",
            "static_type_I_stress",
            "DEC",
            "all_gravitating_source_elements_distance_ge_1m",
            "finite_positive_total_gravitating_energy",
        ],
        "DEC_active_source_abs_over_energy_max":4.0,
        "DEC_negative_active_source_magnitude_over_energy_max":2.0,
        "stress_extremizers":extremizers,
        "min_source_gravitating_energy_J":float(Emin),
        "max_accel_if_source_gravitating_energy_lt_10MJ_m_s2":float(Amax),
        "source_energy_to_10MJ_ratio":float(Emin/ENERGY_CEILING),
        "operating_energy_inference":
            "NOT_DIRECT_UNLESS_GRAVITATING_SOURCE_ENERGY_COUNTS_IN_BUDGET",
        "006D_excluded_from_GR_energy_cost":
            "NO; REFERENCE_REMAINS_COSTLY",
        "theorem_scope":
            "NO_GO_ONLY_IF_ASSUMPTIONS_AND_SOURCE_ENERGY_BUDGET_APPLY",
    }


def verify_dec_inequality():
    rng = np.random.default_rng(42)
    eps = rng.uniform(1e-6,2,size=1000)
    p = rng.uniform(-1,1,size=(1000,3))*eps[:,None]
    S = eps+p.sum(axis=1)
    ratio = np.max(abs(S)/eps)
    neg = np.max(np.maximum(-S,0)/eps)
    if ratio>4+1e-12 or neg>2+1e-12:
        raise AssertionError("DEC_SAMPLES_VIOLATE_ANALYTIC_BOUND")
    return {
        "samples":1000,
        "max_abs_active_stress_ratio":float(ratio),
        "max_negative_active_stress_ratio":float(neg),
    }


def scalar_exchange():
    """Positive-residue canonical universal linear scalar attracts like sources."""
    coupling = .2
    mass = .35
    r = 1.3
    q1 = q2 = 1.0
    V = -coupling**2*q1*q2*np.exp(-mass*r)/(4*np.pi*r)
    force = (
        -coupling**2*q1*q2*np.exp(-mass*r)
        *(1+mass*r)/(4*np.pi*r**2)
    )
    if not (V<0 and force<0):
        raise AssertionError("HEALTHY_LIKE_CHARGE_SCALAR_SIGN_INCORRECT")
    return {
        "canonical_kinetic_residue":"POSITIVE",
        "universal_like_source_potential":float(V),
        "universal_like_source_radial_force":float(force),
        "same_sign_universal_scalar_repulsion":"NO_AT_TREE_LEVEL_LINEAR",
        "opposite_charge_repulsion":
            "POSSIBLE_BUT_NOT_UNIVERSAL_EQUAL_SIGN",
        "wrong_sign_kinetic_repulsion":"GHOST_DISALLOWED",
        "nonlinear_screened_disformal_or_multifield":"NOT_RULED_OUT",
    }


def universal_metric_geometry():
    """Weak conformal metric: a/c²=-grad sigma, tidal geometry from Hessian.

    Gaussian sigma is PRESCRIBED, not sourced from Einstein equations.
    """
    xyz = np.array([1.1,.55,1.3])
    width2 = 3.3
    s0 = 2e-16
    sig = s0*np.exp(-(xyz@xyz)/(2*width2))
    grad = -sig*xyz/width2
    hess = sig*(
        np.outer(xyz,xyz)/width2**2-np.eye(3)/width2
    )
    h = 1e-3
    grad_num = np.array([
        (
            s0*np.exp(
                -((xyz+np.eye(3)[i]*h)@(xyz+np.eye(3)[i]*h))/(2*width2)
            )
            -s0*np.exp(
                -((xyz-np.eye(3)[i]*h)@(xyz-np.eye(3)[i]*h))/(2*width2)
            )
        )/(2*h)
        for i in range(3)
    ])
    if not (
        np.linalg.norm(grad_num-grad)<1e-22
        and np.linalg.norm(hess)>1e-18
    ):
        raise AssertionError("CONFORMAL_GEOMETRY_CHECK_FAIL")
    return {
        "prescribed_metric_profile_only":True,
        "a_over_c2_minus_grad_sigma":(-grad).tolist(),
        "curvature_tidal_hessian_norm":float(np.linalg.norm(hess)),
        "gradient_FD_abs_error":float(np.linalg.norm(grad_num-grad)),
        "neutral_test_metric_sign":"CONDITIONAL_NOT_SOURCED",
        "Einstein_response":"NOT_SOLVED",
        "Earth_down_craft_up":"NOT_DERIVED",
    }


def si_portal_scaling():
    """Portal rescaling degeneracy, NOT a symmetry of the full action.

    Keeping sigma invariant under field unit redefinitions can change
    Maxwell quadratic energy. No physical SI scale follows from P alone.
    """
    ex,by = .03,.04
    alpha,beta = .05,40.
    sx,sy = 3.,2.
    p0 = ex*by
    p1 = (sx*ex)*(sy*by)
    sig0 = alpha*p0-beta*p0*p0
    sig1 = (
        (alpha/(sx*sy))*p1
        -(beta/(sx*sy)**2)*p1*p1
    )
    e0 = .5*(ex**2+by**2)
    e1 = .5*((sx*ex)**2+(sy*by)**2)
    if abs(sig0-sig1)>1e-15 or e0==e1:
        raise AssertionError("PORTAL_SI_NORMALIZATION_SCREEN_FAIL")
    return {
        "portal_sigma_equal_under_rescaling":True,
        "canonical_quadratic_field_cost_ratio":float(e1/e0),
        "status":"PORTAL_ONLY_DEGENERACY_NOT_SYMMETRY_OF_FULL_ACTION",
        "physical_SI_normalization":"NOT_SPECIFIED",
    }


def science(root):
    parent = check_parents(root)
    bianchi = exact_bianchi()
    y = d0_euler_amendment()
    gr = gr_dec_bound()
    dec = verify_dec_inequality()
    sc = scalar_exchange()
    geometry = universal_metric_geometry()
    si = si_portal_scaling()
    return {
        "parents":parent,
        "M0_differential_Y":y,
        "M0_bianchi":bianchi,
        "M0_conditional_neutral_geometry":geometry,
        "SI_portal_scaling_warning":si,
        "M1_GR_DEC_energy":gr,
        "M1_DEC_samples":dec,
        "M2_canonical_scalar_exchange":sc,
        "M3_quantum_reserve":
            "NO_CLOSED_REGULATED_SOURCE_OR_NEW_ASSUMPTION",
        "classification":"SCOPED_IMPOSSIBILITY_CERTIFICATE",
        "hypothesis_matrix":[
            {
                "family":"M0",
                "question":"Is D0 constitutive response a full Y Euler bulk source?",
                "result":"ONLY_IF_GRAD_LAMBDA_WEDGE_FX_NONZERO; MANUFACTURED_OFFSHELL_EXAMPLE",
                "qualified_survivor":False,
            },
            {
                "family":"M1",
                "question":"Can <=10MJ total DEC gravitating source produce 1g at 1m in static linearized GR?",
                "result":"NO_UNDER_DECLARED_SOURCE_ENERGY_AND_DEC_ASSUMPTIONS",
                "qualified_survivor":False,
            },
            {
                "family":"M2",
                "question":"Can one healthy universal equal-sign canonical linear scalar mediate repulsion?",
                "result":"NO_IN_LINEAR_TREE_LEVEL_CANONICAL_CLASS",
                "qualified_survivor":False,
            },
            {
                "family":"M3",
                "question":"Is a regulated new quantum source available to test?",
                "result":"NO_SPECIFIED_ASSUMPTION_NOT_ACTIVATED",
                "qualified_survivor":False,
            },
        ],
        "negative_controls":{
            "constant_lambda_Y_source_zero":True,
            "lambda_function_of_A0_Y_source_zero":True,
            "X_polarity_reverses_manufactured_Y_source":True,
            "DEC_negative_active_stress_bound":True,
            "canonical_scalar_equal_sign_attractive":True,
            "scalar_wrong_sign_kinetic_ghost_excluded":True,
        },
        "R11_rank_two":"INHERITED_SHA_LOCKED_NOT_RECOMPUTED",
        "R8_X_unfitted_exterior_error_fraction":.059614,
        "R9_Y_unfitted_exterior_error_fraction":.208987,
        "gates":{
            "D0_Y_EULER_ERRATUM":
                "DERIVED_DIFFERENTIAL_NECESSARY_CONDITION",
            "M1_STATIC_GR_DEC_BUDGET":
                "SCOPED_RED_IF_TOTAL_SOURCE_ENERGY_LT_10MJ",
            "M2_MINIMAL_HEALTHY_SCALAR":
                "SCOPED_RED_FOR_UNIVERSAL_EQUAL_SIGN_LINEAR",
            "M0_REAL_ONSHELL_SOURCE":"NOT_DERIVED",
            "M0_PH16_NATIVE_CONTINUUM_MATCH":"NOT_DERIVED",
            "FULL_OFFSHELL_ACTION_EARTH_SUPPORT_FLUID":"NOT_DERIVED",
            "FULL_LORENTZIAN_CONSTRAINT_HEALTH":"NOT_CERTIFIED",
            "UNIVERSAL_METRIC_EXTERIOR_EINSTEIN":"NOT_DERIVED",
            "SI_EP_UV":"NOT_CERTIFIED",
            "PORTAL_SI_NORMALIZATION":"NOT_CLOSED",
            "M3_QFT":"RESERVED",
        },
        "qualified_gravity_bridge_survivors":[],
        "M0_conditional_idea":
            "CONTINUED_ONLY_AS_UNDERDETERMINED_HYPOTHESIS",
        "research_maturity_heuristic_before_percent":34,
        "research_maturity_heuristic_after_percent":34,
        "GAMMA1_01_authorized":False,
        "PH16_05_authorized":False,
        "PH17_authorized":False,
        "006D_replaced":False,
        "real_1kg_torus_ge1g_ge1m":"NOT_CERTIFIED",
        "Earth_down":"NOT_DERIVED",
        "whole_craft_up":"NOT_DERIVED",
        "complete_operating_energy_SI_lt10MJ":"NOT_CERTIFIED",
        "next_decision":
            "NO_AUTOMATIC_EXPENSIVE_RUN; REQUIRE_ACTION_LEVEL_ONSHELL_SOURCE_AND_CONTINUUM_EVIDENCE",
        "claims_boundary":
            "M1/M2 are assumption-scoped no-go tests, not universal gravity no-gos",
    }
