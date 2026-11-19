"""GAMMA1-00R2: PH16 saved-data sufficiency and Lorentzian nonuniqueness.

The PH16-04R2 stationary action is NOT a known complete Lorentzian action.
This audit does not repeat its numerical solve, choose a healthy new operator,
or establish real source, Earth reaction, external acceleration, or energy.

A covariant gauge invariant witness uses the neutral fluid four-velocity u:
  Delta L = (eta/2) (u^mu F^Y_mu nu)(u^rho F^Y_rho{}^nu).
For rest-frame magnetostatics F^Y_0i=0, it and all first derivatives
on the static sector vanish, while the transverse Y electric kinetic
changes by eta. It is a LOGICAL COMPLETION WITNESS, NOT A PHYSICAL CANDIDATE.
"""
from __future__ import annotations

import ast
from fractions import Fraction
import hashlib
import math
from pathlib import Path
from typing import Any

import sympy as sp

PH16_SOURCE_SHA = 'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
EXPECTED_CASES = {'12_L12': (12, 12.), '18_L12': (18, 12.), '12_L16': (12, 16.)}


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else 'MISSING'


def source_structure(path: Path) -> dict[str, Any]:
    """Observe final-profile retention in exact PH16 producing code, no import."""
    if hash_file(path) != PH16_SOURCE_SHA:
        raise ValueError('PH16 R2 source hash changed')
    tree = ast.parse(path.read_text())
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    joint = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
    if not {'case', 'report', 'exact_atlas'} <= functions.keys() or 'JointAction' not in joint:
        raise ValueError('PH16 source has unrecognized structure')
    case = functions['case']
    direct_return = [node.value for node in case.body if isinstance(node, ast.Return)]
    if len(direct_return) != 1 or not isinstance(direct_return[0], ast.Dict):
        raise ValueError('Unexpected PH16 case result structure')
    fields = {}
    for key, value in zip(direct_return[0].keys, direct_return[0].values):
        if isinstance(key, ast.Constant) and isinstance(key.value, str):
            fields[key.value] = value
    summary = fields.get('Y_preconditioned_joint')
    if not isinstance(summary, ast.Name) or summary.id != 'pre_solved':
        raise ValueError('Cannot identify PH16 final scalar summary')
    if any(name in fields for name in ('F', 'A', 'Y', 'final_fields', 'pre_x', 'direct_x')):
        raise ValueError('PH16 final fields may have been retained; needs new audit')
    # The returned pre_solved is a diagnostic dict, while pre_x remains local.
    return {
        'case_return_keys': sorted(fields),
        'final_state_arrays_returned': False,
        'final_summary_variable': summary.id,
        'stationary_state_local_only': True,
        'PH16_source_sha256': PH16_SOURCE_SHA,
        'recomputation_performed': False,
    }


def result_sufficiency(doc: dict[str, Any]) -> dict[str, Any]:
    """Audit original immutable R2 result, not fabricated profiles."""
    if doc.get('source_sha256') != PH16_SOURCE_SHA:
        raise ValueError('R2 result source fingerprint mismatch')
    if doc.get('scoped_gates_pass') is not True:
        raise ValueError('R2 historical scoped gates not successful')
    if doc.get('006D_replaced') is not False:
        raise ValueError('R2 historical 006D claim changed')
    if doc.get('whole_craft_Earth_down_craft_up') != 'NOT_DERIVED':
        raise ValueError('R2 historical Earth/craft claim changed')
    science = doc.get('scoped_results', {})
    cases = science.get('cases', {})
    if set(cases) != set(EXPECTED_CASES):
        raise ValueError('Unexpected R2 mesh identities: '+str(sorted(cases)))
    records = {}
    complete_profiles = True
    missing_per_case = {}
    for name, (nr, size) in EXPECTED_CASES.items():
        case = cases[name]
        mesh = case['mesh']
        if int(mesh['nr']) != nr or abs(float(mesh['L'])-size) > 1e-12:
            raise ValueError('R2 mesh metadata mismatch '+name)
        joint = case['Y_preconditioned_joint']
        grad = float(joint['final_residual_L2'])
        if not math.isfinite(grad) or grad >= 1e-6 or joint['root_success'] is not True:
            raise ValueError('R2 stationarity claim not supported '+name)
        if any(abs(float(z)-400.) > 1e-8 for z in joint['N']):
            raise ValueError('R2 fixed Noether N drift '+name)
        frozen = float(joint['frozen_magnetic_margin_min'])
        if not math.isfinite(frozen) or frozen <= 0:
            raise ValueError('R2 frozen magnetic screen drift '+name)
        if joint['frozen_negative_cells'] != 0:
            raise ValueError('R2 frozen negative-cell result drift '+name)
        missing = sorted({'F', 'A', 'Y'} - set(joint))
        missing_per_case[name] = missing
        complete_profiles &= not missing
        records[name] = {
            'joint_residual_L2': grad,
            'stationary_root_success': True,
            'Noether_N': [float(z) for z in joint['N']],
            'frozen_magnetic_margin_min': frozen,
            'frozen_negative_cells': 0,
            'saved_final_field_arrays': not bool(missing),
            'weak_seed_residual_L2': float(case['direct_weak_seed']['final_residual_L2']),
        }
    if complete_profiles:
        raise ValueError('R2 archives full state; insufficient-profile obstruction inapplicable')
    return {
        'cases': records,
        'missing_final_arrays_per_mesh': missing_per_case,
        'all_three_complete_saved_profiles': False,
        'can_evaluate_actual_background_local_kinetic_matrix': False,
        'can_evaluate_full_Lorentzian_constrained_spectrum': False,
        'rerun_of_PH16_performed': False,
        'limitation': 'Verified R2 scalar summaries omit final F[2,N], A[N], Y[N] arrays. A spatial stationary Routhian also lacks a full unique Lorentzian kinetic/constraint action.',
    }


def exact_completion_witness() -> dict[str, Any]:
    """Exact off-shell gauge/covariance witness. NOT a PH16 ghost claim."""
    eta, e, b, k, omega = sp.symbols('eta e b k omega', real=True)
    lag = sp.Rational(1, 2)*(1+eta)*e**2-sp.Rational(1, 2)*b**2
    base = lag.subs(eta, 0)
    delta = sp.expand(lag-base)
    x, y = sp.symbols('x y', real=True)
    gauge = sp.Function('gauge')(x, y)
    kinetic = sp.diff(lag, e, 2)
    dispersion = sp.factor((1+eta)*omega**2-k**2)
    checks = {
        'stationary_magnetostatic_delta_zero': sp.simplify(delta.subs(e, 0)) == 0,
        'stationary_E_first_variation_zero': sp.simplify(sp.diff(delta, e).subs(e, 0)) == 0,
        'stationary_B_first_variation_zero': sp.diff(delta, b) == 0,
        'stationary_metric_and_u_first_variations_zero': sp.simplify(delta.subs(e, 0)) == 0,
        'Y_transverse_electric_hessian_shift_eta': sp.simplify(kinetic-(1+eta)) == 0,
        'gauge_dd_commutator_null': sp.simplify(sp.diff(gauge, x, y)-sp.diff(gauge, y, x)) == 0,
        'Maxwell_eta0_positive': kinetic.subs(eta, 0) == 1,
        'positive_eta2_positive': kinetic.subs(eta, 2) == 3,
        'negative_eta_minus2_negative': kinetic.subs(eta, -2) == -1,
        'mode_dispersion_frozen_fluid': sp.solve(dispersion, omega**2) == [k**2/(eta+1)],
    }
    if not all(checks.values()):
        raise AssertionError('Completion witness exact algebra failed: '+str(checks))
    return {
        'exact_checks': {key: bool(value) for key, value in checks.items()},
        'operator': '(eta/2)*(u^mu F^Y_mu nu)*(u^rho F^Y_rho{}^nu)',
        'role': 'NONUNIQUENESS_COUNTEREXAMPLE_NOT_PROPOSED_NEW_PHYSICS',
        'hypothesis': 'u is a normalized dynamical fluid velocity in a covariant completion; u=(1,0,0,0) in its local rest frame and Y electric components vanish in PH16 magnetostatics',
        'static_delta_L': '0',
        'static_first_EL_variations': '0 within static magnetostatic subspace',
        'eta_values_and_transverse_electric_coeff': {'eta_minus2': -1, 'eta_zero': 1, 'eta_plus2': 3},
        'transverse_dispersion_frozen_u': '(1+eta)*omega^2=k^2; eta=-2 has nonpositive kinetic/unstable dispersion in this witness',
        'result': 'Same stationary fields and first variations, different Lorentzian electric principal symbols',
        'not_established': 'No on-shell PH16 ghost, no real fluid completion, no actual full constraint spectrum, no Einstein or SI prediction',
    }


def independent_fraction_check() -> dict[str, Any]:
    """Finite-difference diagnostic with exact rational arithmetic."""
    h = Fraction(1, 1024)
    results = {}
    for eta in (-2, 0, 2):
        def L(e: Fraction) -> Fraction:
            return Fraction(1+eta, 2)*e*e
        curvature = (L(h)-2*L(Fraction(0))+L(-h))/(h*h)
        if curvature != 1+eta:
            raise AssertionError('Independent rational curvature mismatch')
        results[str(eta)] = int(curvature)
    return results


def result_atlas(doc: dict[str, Any], parent_source: Path) -> dict[str, Any]:
    source = source_structure(parent_source)
    saved = result_sufficiency(doc)
    witness = exact_completion_witness()
    rational = independent_fraction_check()
    if rational != {'-2': -1, '0': 1, '2': 3}:
        raise AssertionError('Rational independent control drift')
    return {
        'experiment': 'GAMMA1-00R2_STATIONARY_TO_LORENTZIAN_COMPLETION_GATE',
        'scope': 'EXACT_LOCAL_COUNTEREXAMPLE_PLUS_ORIGINAL_SAVED_RESULT_AUDIT_NO_PDE',
        'PH16_source_structure': source,
        'PH16_R2_saved_data': saved,
        'covariant_completion_nonuniqueness': witness,
        'independent_fraction_electric_hessian': rational,
        'negative_controls': {
            'eta_0': 'canonical Maxwell electric kinetic coefficient +1',
            'eta_plus2': 'alternative healthy-looking local electric coefficient +3, not full health',
            'eta_minus2': 'alternative negative electric coefficient -1, NOT PH16 instability',
            'E_Y_zero': 'all completion terms vanish on static PH16 Y-magnetic ansatz',
            'gauge': 'depends on F_Y, not A_Y directly; dd(gauge)=0',
            'spatial_data_inadequacy': 'scalar maxima/minima cannot be inverted to full final fields',
        },
        'M0_actual_stationary_background_ghost': 'NOT_ESTABLISHED',
        'M0_full_modes_from_archived_R2': 'NOT_DETERMINABLE',
        'M0_same_covariant_action': 'NOT_SPECIFIED_BY_R2_ROUTHIAN',
        'Einstein_metric': 'NOT_SOLVED',
        'true_exterior': 'NOT_CERTIFIED',
        'Earth_down': 'NOT_DERIVED',
        'whole_craft_up': 'NOT_DERIVED',
        'torus_1kg_1g_1m': 'NOT_CERTIFIED',
        'complete_SI_energy_lt10MJ': 'NOT_CERTIFIED',
        '006D_replaced': False,
        'qualified_physical_survivors': [],
        'GAMMA1_01_authorized': False,
        'PH16_05_authorized': False,
        'PH17_authorized': False,
        'decision': 'STOP_REPEATING_OFFSHELL_TESTS_SPECIFY_COVARIANT_ACTION_AND_SAVE_PROFILES_FIRST',
        'scientific_classification': 'PASS_SCOPED_NONUNIQUENESS_AND_EVIDENCE_SUFFICIENCY',
        'next_physics_contract': [
            'Define unique covariant time-derivative and boundary terms and full dynamical fluid/charged-scalar source plus universal Earth/hull/support actions',
            'Export immutable native Fplus/Fminus, A_X, A_Y arrays from an original stationary physical solve without changing its equations; record profiles per mesh, hashes, units, boundary conditions and gauge',
            'Then perform gauge-reduced Lorentzian principal symbol and constrained Schur/characteristic spectrum on that archived source, not prescribed trials',
            'Derive Einstein/exterior and complete Earth-down/whole-craft-up force ledger independently before further promotion',
        ],
    }
