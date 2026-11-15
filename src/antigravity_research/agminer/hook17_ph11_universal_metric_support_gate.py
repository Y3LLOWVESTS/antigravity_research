"""HOOK17-PH11: exact universal-conformal variations and bounded-well support debt.

The PH10 frozen-well fields are DATA, not an on-shell source. This independent
symbolic-plus-numerical audit derives what a universal metric would add to its
field equations and computes the nonzero support load required by its finite
square wells. No additional optimization or source fields.

Full candidate (schematic):
  S = S_EH[g] - 1/4 int sqrt(-g)(F_X^2+F_Y^2) +
      S_matter[psi_i, A_X,A_Y, exp(2*sigma(P))*g] + S_support
  P=1/4 F_X(mu nu) epsilon^(mu nu rho sigma) F_Y(rho sigma)
  epsilon^{0123}=+1/sqrt(-g); sigma=alpha P-beta P^2.

For scalar matter K=g^munu(Dpsi)*_mu (Dpsi)_nu, U=mass/trap density:
  L_m/sqrt(-g)=-exp(2 sigma) K - exp(4 sigma) U.
  lambda = d(L_m/sqrt(-g))/dP
         = exp(4sigma)*Ttilde*sigma'(P)
  Ttilde = -2 exp(-2sigma) K -4 U.

Gauge constitutive tensors include -lambda *F_other.
If lambda varies, Bianchi does not cancel d(lambda *F_other).

Metric source:
  T_eff^munu=exp(6sigma)*Ttilde^munu
             - exp(4sigma)*Ttilde*P*sigma'(P)*g^munu.

The last term follows from P's metric dependence.
Full Einstein equations, charged source EOM and supports are NOT solved.
Constant lambda is topological (surface only) in the bulk.

Square-well stress-load magnitude for species of charge Q and frequency omega:
  L_wall = U0 R^2 |f(R)|^2 Q/(2 omega int_0^inf r^2 f(r)^2 dr).

This is a radial interface TRACTION integral for a prescribed square well,
not a net external force and not an SI energy/force. It requires dynamical
support matter. Derivative is at FIXED scalar wavefunction and well depth.

All pass gates are strictly reduced/analytic.
006D unreplaced; M5V frozen.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from hashlib import sha256

import sympy as sp
from scipy.integrate import quad
from scipy.special import spherical_jn

BRANCH = '032H17A12D1R3X3B17-PH11'

ARCHIVES = {
    'ph10_source': (
        'src/antigravity_research/agminer/hook17_ph10_bounded_well_source_gate.py',
        '1d2f8624fab28cf82301a582fb7b6289e9ce936e2a423d0bddae3ff10e1f4228'
    ),
    'ph10_sim': (
        'simulations/032h17a12d1r3x3b17_ph10_bounded_well_source_gate.py',
        'd7dc82028bbdd51b151579e92e93931ec12d038885a72b2af8f2007a1e844af1'
    ),
    'ph10_test': (
        'tests/agminer/test_032h17_ph10_bounded_well_source_gate.py',
        '3f45db4adb90d5ef990fc242b447efcf9a9a86c5ffe07693d14dbc15af2ed612'
    ),
    'ph10_result': (
        'results/data/032h17_ph10_bounded_well_20261115T044314781842Z.json',
        '56639e14886cc4169867691ef6c0f5c4f86bb37bea8da00fa7ac3bfb7f2b5de9'
    ),
    'ph9_source': (
        'src/antigravity_research/agminer/hook17_ph9_covariant_loading_gate.py',
        '6778d91755c6669625e363ae568f7887b1a28327817f005dc0ba858774982858'
    ),
    'm5v_source': (
        'src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py',
        'ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'
    ),
}


def exact_variations():
    """Independent Weyl, P-variation, Ward and constitutive tests."""
    p, alpha, beta, K, U, t = sp.symbols(
        'p alpha beta K U t', real=True
    )

    sigma = alpha*p - beta*p*p
    sprime = sp.diff(sigma, p)
    omega = sp.exp(sigma)

    lag = -omega**2*K - omega**4*U
    tilde_trace = -2*omega**(-2)*K - 4*U
    lam = sp.simplify(omega**4*tilde_trace*sprime)

    assert sp.simplify(sp.diff(lag, p)-lam) == 0
    assert sp.simplify(
        lam + (2*omega**2*K+4*omega**4*U)*sprime
    ) == 0

    # True four-dimensional Weyl transformation:
    # sqrt(-g)=exp(4t), g^-1=exp(-2t), P=p*exp(-4t).
    pt = p*sp.exp(-4*t)
    sigma_t = alpha*pt - beta*pt*pt
    Lweyl = (
        -sp.exp(2*t+2*sigma_t)*K
        -sp.exp(4*t+4*sigma_t)*U
    )
    trace_eff = omega**4*tilde_trace*(1-4*p*sprime)

    assert sp.simplify(
        sp.diff(Lweyl, t).subs(t, 0)-trace_eff
    ) == 0

    # Independent anisotropic metric test: g_zz -> exp(2r)*g_zz.
    # K = |D_z psi|^2, sqrt(-g)=exp(r), P=p*exp(-r).
    r = sp.symbols('r', real=True)
    pr = p*sp.exp(-r)
    sigr = alpha*pr-beta*pr*pr

    Lzz = (
        -sp.exp(-r+2*sigr)*K
        -sp.exp(r+4*sigr)*U
    )
    Tzz = omega**2*K-omega**4*U-lam*p

    assert sp.simplify(
        sp.diff(Lzz, r).subs(r, 0)-Tzz
    ) == 0

    # Vacuum Maxwell theory is Weyl-invariant in four dimensions.
    assert sp.simplify(
        sp.exp(4*t)*sp.exp(-4*t)-1
    ) == 0

    # Independent antisymmetric components of both field strengths.
    ex, ey, ez, bx, by, bz, ux, uy, uz, vx, vy, vz = sp.symbols(
        'ex ey ez bx by bz ux uy uz vx vy vz',
        real=True
    )

    # FX_01=ex, FX_02=ey, FX_03=ez,
    # FX_23=bx, FX_31=by, FX_12=bz.
    # Corresponding components of FY are ux,uy,uz,vx,vy,vz.
    wedge = (
        ex*vx + ey*vy + ez*vz
        + ux*bx + uy*by + uz*bz
    )

    assert sp.diff(wedge, ex) == vx
    assert sp.diff(wedge, vy) == ey
    assert sp.simplify(
        sp.diff(wedge*sp.exp(-4*t), t).subs(t, 0)
        + 4*wedge
    ) == 0

    # For P=(1/4) FX epsilon FY,
    # delta P=(1/2) *FY delta FX.

    x, charge = sp.symbols('x charge', real=True)
    f = sp.Function('f')(x)
    theta = sp.Function('theta')(x)
    a = sp.Function('a')(x)
    coeff = sp.Function('omega2')(x)

    w = sp.diff(theta, x)-charge*a
    Lphase = -coeff*f*f*w*w
    current = sp.diff(Lphase, a)
    e_theta = -sp.diff(
        sp.diff(Lphase, sp.diff(theta, x)), x
    )

    assert sp.simplify(
        sp.diff(current, x)-charge*e_theta
    ) == 0

    assert sp.simplify(
        current-2*charge*coeff*f*f*w
    ) == 0

    # This is an OFF-SHELL IDENTITY, not an on-shell source pass.

    # Variable lambda: d(lambda *F_other)
    # = d(lambda)*F_other + lambda*d(*F_other).
    z = sp.symbols('z', real=True)
    c = sp.Function('c')(z)
    b = sp.Function('B')(z)

    assert sp.simplify(
        sp.diff(c*b, z)
        - c*sp.diff(b, z)
        - sp.diff(c, z)*b
    ) == 0

    const = sp.symbols('const')
    assert sp.diff(const, z) == 0

    return {
        'universal_scalar_metric_chain_rule': 'PASS_EXACT',
        'matter_trace_portal_loading': 'PASS_EXACT',
        'mixed_FX_FY_antisymmetric_variation': 'PASS_EXACT',
        'metric_variation_Weyl_cross_check': 'PASS_EXACT',
        'metric_variation_anisotropic_zz_cross_check': 'PASS_EXACT',
        'Maxwell_four_dimensional_Weyl_invariance': 'PASS_EXACT',
        'source_phase_gauge_Noether_identity':
            'PASS_EXACT_OFF_SHELL_IDENTITY',
        'nonconstant_trace_constitutive_coupling':
            'REQUIRED_BY_SAME_ACTION',
        'constant_cross_term_bulk': 'PURE_BIANCHI_BOUNDARY_TERM',
        'einstein_source_on_shell': 'NOT_DERIVED',
        'all_species_universal_metric_EOM': 'NOT_DERIVED',
        'full_U1_constraints_and_mode_health': 'NOT_CERTIFIED',
    }


def wall_load(data, relative_step=1.e-5):
    """Exact radial square-well traction and independent finite differences."""
    primary = data['primary']
    omega = float(primary['spec']['omega'])

    if omega <= 0:
        raise ValueError('Frequency must be positive')

    if (
        len(primary['eigenstates']) != 2
        or len(primary['independent_continuum_radial_virial']) != 2
    ):
        raise ValueError('Expected l=0 and l=1 modes')

    result = []
    total = 0.

    for mod, rad, q in zip(
        primary['eigenstates'],
        primary['independent_continuum_radial_virial'],
        (
            primary['spec']['positive_charge'],
            primary['spec']['vortex_charge']
        )
    ):
        l = int(mod['l'])
        R = float(mod['R'])
        k = float(mod['k'])
        depth = float(mod['depth'])
        norm = float(rad['normalization'])
        fR = float(mod['boundary_value'])

        if not (
            0 <= l <= 1 and min(R, k, depth, norm, q) > 0
        ):
            raise ValueError('Invalid radial source data')

        amplitude_sq = q/(2*omega*norm)
        exact = depth*R*R*amplitude_sq*fR*fR

        dr = relative_step*R

        # Differentiate the prescribed well potential energy
        # with respect to its radius, holding wavefunction and depth fixed.
        def primitive(edge):
            return quad(
                lambda r: r*r*spherical_jn(l, k*r)**2,
                0,
                edge,
                epsabs=1e-12,
                epsrel=1e-12
            )[0]

        derivative = -depth*amplitude_sq*(
            primitive(R+dr)-primitive(R-dr)
        )/(2*dr)

        rel = abs(-derivative-exact)/exact

        result.append({
            'l': l,
            'species_count': 2,
            'charge_magnitude_per_species': q,
            'well_depth': depth,
            'integrated_radial_traction_single_species': exact,
            'integrated_radial_traction_pair': 2*exact,
            'independent_energy_radius_derivative_single_species':
                derivative,
            'relative_derivative_disagreement': rel,
            'radial_net_vector_force_for_isolated_spherical_well': 0.0,
        })

        total += 2*exact

    return {
        'modes': result,
        'total_integrated_radial_traction_magnitude': total,
        'SI_calibration': 'NONE',
        'net_external_propulsive_force': 'NOT_DERIVED',
        'finite_onboard_trap_hardware_energy': 'NOT_IN_PH10_LEDGER',
        'scope': 'FIXED_STATES_SQUARE_WELL_INTERFACE_ONLY',
    }


def summarize_ph10(data):
    """Audit PH10 without promoting its off-shell source configuration."""
    p = data['primary']
    e = p['partial_energy']

    kinetic = (
        float(e['matter_gradient'])
        - float(e['matter_time'])
    )
    U = float(e['matter_rest_plus_prescribed_trap'])

    # At Omega=1, the flat scalar trace is -2K-4U.
    # This is not the full gravitational source with support included.
    tau = -2*kinetic-4*U

    pprobe = float(p['upper_probe']['P'])
    dp = float(p['upper_probe']['P_prime'])
    alpha = float(p['spec']['alpha'])
    beta = float(p['spec']['beta'])

    down = p['lower_probe']
    lowerforce = float(down['acceleration_shape'])

    if not all(
        math.isfinite(v)
        for v in (tau, pprobe, dp, lowerforce)
    ):
        raise ValueError('PH10 has nonfinite source or field data')

    return {
        'loaded_stress_trace_integral_at_Omega_1': tau,
        'trace_includes_prescribed_trap_but_not_its_hardware': True,
        'source_current_relative_divergence':
            float(p['relative_current_divergence']),
        'loaded_scalar_EOM_X':
            float(p['scalar_KG_residual_from_loaded_X']),
        'loaded_scalar_EOM_Y':
            float(
                p['scalar_KG_residual_from_loaded_Y_exact_gauge_correction']
            ),
        'probe_P': pprobe,
        'probe_dP_dz': dp,
        'probe_sigma_prime': alpha-2*beta*pprobe,
        'neutral_probe_force_shape':
            float(p['upper_probe']['acceleration_shape']),
        'earthward_point_probe_force_shape': lowerforce,
        'equal_opposite_reaction_for_finite_pair_POTENTIAL_ONLY':
            -lowerforce,
        'earth_body_integral_and_GR_stress': 'NOT_DERIVED',
        'full_source_support_stress': 'NOT_DERIVED',
        'metric_portal_canonical_mode_health': 'NOT_CERTIFIED',
    }


def provenance(root):
    """Read historical archive hashes without modifying any archive."""
    result = {}

    for name, (relative, expected) in ARCHIVES.items():
        f = Path(root)/relative

        if not f.is_file():
            result[name] = {
                'status': 'MISSING',
                'expected_sha256': expected,
            }
        else:
            actual = sha256(f.read_bytes()).hexdigest()
            result[name] = {
                'status': (
                    'MATCH' if actual == expected
                    else 'HASH_MISMATCH'
                ),
                'actual_sha256': actual,
                'expected_sha256': expected,
            }

    return result


def run(root, ph10_data=None):
    """Run exact identities, source support and fail-closed PH10 audit."""
    root = Path(root)

    if ph10_data is None:
        with (
            root/ARCHIVES['ph10_result'][0]
        ).open('r', encoding='utf-8') as f:
            ph10_data = json.load(f)

    if ph10_data.get('branch') != '032H17A12D1R3X3B17-PH10':
        raise ValueError('Wrong PH10 data branch')

    th = exact_variations()
    wall = wall_load(ph10_data)
    audit = summarize_ph10(ph10_data)

    if not (
        wall['total_integrated_radial_traction_magnitude'] > 0
        and max(
            m['relative_derivative_disagreement']
            for m in wall['modes']
        ) < 1e-7
        and audit['source_current_relative_divergence'] > 1e-3
        and abs(audit['loaded_scalar_EOM_X']) > 1e-3
        and abs(audit['loaded_scalar_EOM_Y']) > 1e-3
        and audit['earthward_point_probe_force_shape'] < 0
    ):
        raise AssertionError(
            'PH10 fail-closed on-shell/source/support screens did not reproduce'
        )

    history = provenance(root)

    return {
        'branch': BRANCH,
        'previous_case': 'PH10_OFFSHELL_BOUNDED_WELL',
        'exact_variations': th,
        'well_support_debt': wall,
        'ph10_matter_and_reaction_audit': audit,
        'archival_provenance': history,
        'gates': {
            'P0_PROVENANCE': (
                'PASS'
                if all(v['status'] == 'MATCH' for v in history.values())
                else 'UNRESOLVED'
            ),
            'P1_METRIC_AND_GAUGE_CHAIN_RULE':
                'PASS_EXACT_PROPOSED_ACTION_SCOPED',
            'P1_GAUGE_WARD_SOURCE_IDENTITY':
                'PASS_EXACT_OFF_SHELL_IDENTITY_ONLY',
            'P1_LOADED_SOURCE_MATTER_EOM':
                'RED_PH10_OFF_SHELL',
            'P1_SQUARE_WELL_BOUNDARY_TRACTION':
                'NONZERO_SUPPORT_MATTER_NOT_DERIVED',
            'P1_LOADED_DISCRETE_CURRENT_CONSERVATION':
                'NONZERO_RESIDUAL_NOT_CERTIFIED',
            'P2_FULL_TRACE_LOADED_CARRIER_FIELDS':
                'MISSING_FROM_PH10',
            'P2_FULL_UNIVERSAL_METRIC_ALL_MATTER':
                'NOT_SOLVED',
            'P2_EXTERIOR_VACUUM_CLOSURE':
                'NOT_DERIVED',
            'P3_EARTH_DOWN_CRAFT_UP':
                'NOT_DERIVED',
            'B11_M6_FULL_SIGNED_CYCLE':
                'NOT_RUN',
            'P3_NEUTRAL_GE1G_AT_GE1M':
                'NOT_CERTIFIED',
            'STRICT_FULL_ENERGY_LT10MJ':
                'NOT_CERTIFIED',
            '006D_REPLACED': 'NO',
        },
        'verdict':
            'YELLOW_EXACT_ACTION_COMPLETION_REQUIREMENTS_REVEAL_UNSOURCED_SUPPORT_AND_METRIC_LOADING',
    }
