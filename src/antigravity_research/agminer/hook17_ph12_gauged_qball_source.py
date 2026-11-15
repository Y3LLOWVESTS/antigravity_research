"""HOOK17-PH12 — Trap-free gauged scalar source feasibility.

PURPOSE
-------
Replace the PH10 prescribed square-well source with a source solving
its own canonical charged-scalar and Maxwell equations.

Gauged Q-balls are established field-theory solutions, not a newly
discovered source of antigravity. This run tests one proposed source
subsector against conservation, energy, stress and numerical convergence.

ACTION
------
Mostly-plus flat-spacetime signature, natural units:

    L = -|D psi|² - U(|psi|²) - F²/4
    D = partial - i*e*A
    U(s) = m²*s - b*s² + c*s³

Use the stationary spherical ansatz

    psi(t,r) = f(r)*exp(i*omega*t)
    A = A0(r) dt
    W = omega-e*A0

The coupled Euler-Lagrange equations are

    f''+2*f'/r = (m²-W²)*f -2*b*f³+3*c*f⁵
    A0''+2*A0'/r = -2*e*W*f²

For m=1 and b=c=2, U(s)>=s/2 for all s>=0.

Use regular origin conditions and Yukawa/Coulomb Robin conditions
at a large numerical radius R. Scalar tails are exponentially small,
not identically zero. The Robin scalar approximation omits subleading
Coulomb corrections; domain convergence is required.

ELECTRIC CHARGE AND ENERGY
--------------------------
    J0 = 2*e*W*f²
    N = 8*pi*integral(r² W f² dr)
    Q = e*N

    E = 4*pi*integral[
        r²*(W²*f² + f'² + U(f²) + A0'²/2) dr
    ] + Q²/(8*pi*R)

The final term includes the approximate exterior Coulomb energy.
Nonzero scalar tails beyond R are not included exactly.

Check local radial stress conservation and integrated spatial-stress
virial, with the exterior Maxwell contribution.

E/N<m is a necessary energetic free-particle binding screen only.
It is NOT a proof of radial, orbital, classical or quantum stability.

The isolated charged lump is not a gauge-neutral spacecraft source.
A charge-conjugate isolated solution exists, but two separated lumps
have an attractive electromagnetic force and have NOT been jointly
solved. No spinning magnetic Y carrier or full metric system is solved.

The phi^6 theory is an unverified effective source theory. No source
particle has been identified experimentally. No SI-energy scaling,
Earth coupling, gravity, stable pulse, or whole-craft lift is derived.

006D remains unreplaced. ALPHA-1 M5V remains frozen.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, replace
from hashlib import sha256
from pathlib import Path
import math

import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp

BRANCH = "032H17A12D1R3X3B17-PH12"

ARCHIVES = {
    "ph11_source": (
        "src/antigravity_research/agminer/"
        "hook17_ph11_universal_metric_support_gate.py",
        "03e2f18b9d382f7503a41735cf3a709930952a37b60d0bb2b13f7aef281280ba",
    ),
    "ph11_result": (
        "results/data/"
        "032h17_ph11_universal_metric_support_20261115T064702093364Z.json",
        "9593ec23fee787db536e2d1bba111c610ef5d3f0a7c8f91e7e5e2fb8bf53da41",
    ),
    "ph10_source": (
        "src/antigravity_research/agminer/"
        "hook17_ph10_bounded_well_source_gate.py",
        "1d2f8624fab28cf82301a582fb7b6289e9ce936e2a423d0bddae3ff10e1f4228",
    ),
    "m5v_source": (
        "src/antigravity_research/agminer/"
        "hook17_r3b_m5v_unified_exterior_action.py",
        "ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f",
    ),
}


@dataclass(frozen=True)
class Spec:
    scalar_mass: float = 1.0
    quartic: float = 2.0
    sextic: float = 2.0
    gauge_coupling: float = 0.05
    center_amplitude: float = 0.70
    radius: float = 40.0
    grid_nodes: int = 440
    tolerance: float = 1.e-6


def validate(s: Spec):
    if s.grid_nodes < 180:
        raise ValueError("Need at least 180 grid nodes")
    if (
        s.scalar_mass <= 0
        or s.sextic <= 0
        or s.quartic <= 0
        or s.radius < 18
        or s.tolerance <= 0
    ):
        raise ValueError("Invalid matter or geometry")
    if s.gauge_coupling < 0 or s.center_amplitude <= 0:
        raise ValueError("Invalid coupling or amplitude")
    if not all(math.isfinite(v) for v in asdict(s).values()):
        raise ValueError("All parameters must be finite")
    if s.scalar_mass**2 <= s.quartic**2/(4*s.sextic):
        raise ValueError("Potential lacks strictly positive quadratic bound")


def exact_action_identities():
    """Check source current, EOM, Ward, kinetic and portal symmetry."""
    f, g, A, a, w, e, m, b, c = sp.symbols(
        "f g A a w e m b c", real=True
    )
    U = m*m*f*f-b*f**4+c*f**6
    W = w-e*A
    L = W*W*f*f-g*g-U+a*a/2

    charge = -sp.diff(L, A)
    assert sp.simplify(charge-2*e*W*f*f) == 0

    dU = sp.simplify(sp.diff(U, f)/(2*f))
    assert sp.simplify(
        dU-(m*m-2*b*f*f+3*c*f**4)
    ) == 0

    rhs = sp.simplify((dU-W**2)*f)
    assert sp.simplify(
        rhs-((m*m-W**2)*f-2*b*f**3+3*c*f**5)
    ) == 0
    assert sp.simplify(-sp.diff(L,f)/2-rhs) == 0

    k = sp.symbols("k", real=True)
    assert sp.simplify(
        (w+e*k)-e*(A+k)-W
    ) == 0

    z = sp.symbols("z", nonnegative=True)
    assert sp.simplify(
        z-2*z*z+2*z**3-z/2-z*(2*z-1)**2/2
    ) == 0

    # Positive canonical velocity Hessian before gauge reduction.
    vu, vv, va, vb = sp.symbols(
        "vu vv va vb", real=True
    )
    u0, v0 = sp.symbols("u0 v0", real=True)
    kinetic = (
        (vu+e*A*v0)**2
        +(vv-e*A*u0)**2
        +(va*va+vb*vb)/2
    )
    assert sp.hessian(
        kinetic, [vu,vv,va,vb]
    ) == sp.diag(2,2,1,1)

    # A genuine off-shell phase/gauge Noether identity.
    x,q = sp.symbols("x q", real=True)
    amp = sp.Function("amp")(x)
    phase = sp.Function("phase")(x)
    potential = sp.Function("potential")(x)
    cov = sp.diff(phase,x)-q*potential
    Lphase = -amp*amp*cov*cov
    J = sp.diff(Lphase,potential)
    Ephase = -sp.diff(
        sp.diff(Lphase,sp.diff(phase,x)),x
    )
    assert sp.simplify(
        sp.diff(J,x)-q*Ephase
    ) == 0

    # At FY=0, a radial electric FX and radial trace coefficient
    # obey grad(lambda) cross E_X = 0. This is ONLY the spherical
    # electric subsector, not the completed mixed-source model.
    nx,ny,nz,F,G = sp.symbols(
        "nx ny nz F G", real=True
    )
    E = sp.Matrix([F*nx,F*ny,F*nz])
    gradlambda = sp.Matrix([G*nx,G*ny,G*nz])
    assert gradlambda.cross(E) == sp.zeros(3,1)

    return {
        "canonical_gauged_scalar_current": "PASS_EXACT",
        "charged_scalar_Euler_Lagrange_equation": "PASS_EXACT",
        "electrostatic_Gauss_action_derivative": "PASS_EXACT",
        "gauge_phase_Ward_identity": "PASS_EXACT_OFF_SHELL",
        "stationary_gauge_covariance": "PASS_EXACT",
        "potential_energy_positive_all_amplitudes": "PASS_m1_b2_c2",
        "canonical_kinetic_principal_blocks":
            "PASS_BEFORE_GAUSS_CONSTRAINT",
        "radial_mixed_portal_Y_variation":
            "PASS_ONLY_SPHERICAL_ELECTROSTATIC_SUBSECTOR",
        "nonradial_mixed_portal_Y_variation":
            "UNPROTECTED_BY_SYMMETRY",
        "UV_completion_of_phi6": "NOT_DERIVED",
        "full_gravitational_coupling": "NOT_DERIVED",
    }


def solve(s: Spec = Spec(), charge_sign: int = 1):
    """Solve coupled radial scalar and Maxwell boundary equations."""
    validate(s)

    if charge_sign not in (-1,1):
        raise ValueError("charge_sign must be +/-1")

    m=s.scalar_mass
    b=s.quartic
    c=s.sextic
    e=s.gauge_coupling*charge_sign
    r=np.linspace(0,s.radius,s.grid_nodes)

    def rhs(rr,y,p):
        w=p[0]
        f,df,A,dA=y
        W=w-e*A
        fsource=(m*m-W*W)*f-2*b*f**3+3*c*f**5
        Asource=-2*e*W*f*f

        df_over_r=np.divide(
            df,rr,out=np.zeros_like(df),where=rr>0
        )
        dA_over_r=np.divide(
            dA,rr,out=np.zeros_like(dA),where=rr>0
        )

        return np.array([
            df,
            np.where(rr>0,fsource-2*df_over_r,fsource/3),
            dA,
            np.where(rr>0,Asource-2*dA_over_r,Asource/3),
        ])

    def bc(y0,yR,p):
        w=p[0]
        kappa=math.sqrt(max(1e-12,m*m-w*w))
        return np.array([
            y0[0]-s.center_amplitude,
            y0[1],
            y0[3],
            yR[1]+(kappa+1/s.radius)*yR[0],
            yR[3]+yR[2]/s.radius,
        ])

    width=3.0
    seed=s.center_amplitude*np.exp(-(r/width)**2)
    Aseed=.15*e*np.exp(-(r/8)**2)
    initial=np.array([
        seed,
        -2*r/width**2*seed,
        Aseed,
        -2*r/(8*8)*Aseed,
    ])

    sol=solve_bvp(
        rhs,bc,r,initial,p=np.array([.92*m]),
        tol=s.tolerance,max_nodes=14000,verbose=0
    )

    if sol.status!=0 or not np.isfinite(sol.p[0]):
        raise RuntimeError(
            "Gauged scalar BVP failed: "+sol.message
        )
    if not 0<sol.p[0]<m:
        raise RuntimeError("Not a localized submass-frequency case")

    rr=np.linspace(0,s.radius,5001)
    f,g,A,h=sol.sol(rr)
    w=float(sol.p[0])
    W=w-e*A
    volume=4*np.pi*rr**2

    if (
        np.min(f)<-1e-8
        or np.min(W)<=0
        or not np.isfinite([f,g,A,h]).all()
    ):
        raise RuntimeError("Invalid radial solution")

    U=m*m*f*f-b*f**4+c*f**6
    N=float(np.trapezoid(volume*2*W*f*f,rr))
    Q=e*N

    gauss_flux=4*np.pi*s.radius**2*(-h[-1])
    Efield_inside=float(
        np.trapezoid(volume*h*h/2,rr)
    )
    Efield_outside=Q*Q/(8*np.pi*s.radius)

    Etime=float(np.trapezoid(volume*W*W*f*f,rr))
    Egrad=float(np.trapezoid(volume*g*g,rr))
    Epot=float(np.trapezoid(volume*U,rr))
    Etot=Etime+Egrad+Epot+Efield_inside+Efield_outside

    virial_inside=float(np.trapezoid(
        volume*(3*W*W*f*f-g*g-3*U+h*h/2),rr
    ))
    virial_total=virial_inside+Efield_outside

    Trr=W*W*f*f+g*g-U-h*h/2
    Ttheta=W*W*f*f-g*g-U+h*h/2

    deriv=sol.sol(rr,1)
    dW=-e*h
    dU=2*m*m*f-4*b*f**3+6*c*f**5
    dTrr=(
        2*W*dW*f*f+2*W*W*f*g
        +2*g*deriv[1]-dU*g-h*deriv[3]
    )

    positive=rr>0
    divergence=(
        dTrr[positive]
        +2*(Trr[positive]-Ttheta[positive])/rr[positive]
    )

    stress_error=float(
        np.max(np.abs(divergence[4:]))
    )
    boundary_virial=4*np.pi*s.radius**3*Trr[-1]

    return {
        "spec":asdict(s),
        "charge_sign":charge_sign,
        "omega":w,
        "BVP_status":"SOLVED",
        "BVP_max_collocation_rms":
            float(np.max(sol.rms_residuals)),
        "BVP_mesh_nodes":len(sol.x),
        "A0_at_center":float(A[0]),
        "A0_at_boundary":float(A[-1]),
        "center_f":float(f[0]),
        "tail_f_at_radius":float(f[-1]),
        "tail_f_relative":float(f[-1]/f[0]),
        "positive_radial_mode":bool(np.min(f)>=-1e-8),
        "gauss_flux_at_boundary":float(gauss_flux),
        "gauge_charge_integrated":float(Q),
        "relative_gauss_flux_error":(
            abs(gauss_flux-Q)/max(abs(Q),1e-15)
            if e!=0 else None
        ),
        "Noether_number":N,
        "canonical_energy":{
            "matter_time":Etime,
            "matter_gradient":Egrad,
            "positive_scalar_potential":Epot,
            "electric_inside":Efield_inside,
            "electric_Coulomb_outside":Efield_outside,
            "scalar_plus_electromagnetic_total_including_Coulomb_tail":Etot,
            "energy_per_Noether_number":Etot/N,
            "free_quantum_rest_mass_comparison":m,
        },
        "integrated_spatial_trace_inside":virial_inside,
        "integrated_spatial_trace_plus_Coulomb_tail":virial_total,
        "relative_integrated_stress_defect":
            abs(virial_total)/Etot,
        "exact_radial_stress_balance_max_residual":
            stress_error,
        "virial_boundary_surface_term":float(boundary_virial),
        "virial_boundary_relative_error":
            abs(virial_inside-boundary_virial)/Etot,
        "no_external_square_well":True,
        "one_electric_U1_sector_only":True,
        "complete_microscopic_source_UV":"NOT_CERTIFIED",
        "full_radial_spectral_stability":"NOT_CERTIFIED",
        "two_center_gauge_neutral_on_shell":"NOT_SOLVED",
        "spinning_magnetic_Y_source_on_shell":"NOT_SOLVED",
        "universal_metric_portal_and_Earth":"NOT_SOLVED",
        "SI_energy_and_1g_1m":"NOT_CERTIFIED",
    }


def archive_status(root):
    """Fail-closed SHA-256 provenance for protected previous research."""
    result={}
    for label,(relative,expected) in ARCHIVES.items():
        path=Path(root)/relative
        if not path.is_file():
            result[label]={
                "status":"MISSING",
                "expected_sha256":expected,
            }
            continue
        actual=sha256(path.read_bytes()).hexdigest()
        result[label]={
            "status":(
                "MATCH" if actual==expected
                else "HASH_MISMATCH"
            ),
            "actual_sha256":actual,
            "expected_sha256":expected,
        }
    return result


def run(root):
    """Run pre-specified physical source and numerical-negative controls."""
    exact=exact_action_identities()
    base=Spec()
    primary=solve(base)

    # No optimizer. Each experiment tests one physical assumption.
    farther=solve(replace(base,radius=48.0))
    low=solve(replace(base,center_amplitude=.68))
    high=solve(replace(base,center_amplitude=.72))
    global_U1=solve(replace(base,gauge_coupling=0.0))
    weak=solve(replace(base,center_amplitude=.55))
    stronger_gauge=solve(replace(base,gauge_coupling=.2))
    conjugate=solve(base,charge_sign=-1)

    meshes={
        n:solve(replace(base,grid_nodes=n,tolerance=1e-8))
        for n in (220,440,880)
    }

    def EperN(x):
        return x["canonical_energy"]["energy_per_Noether_number"]

    assert (
        max(x["omega"] for x in meshes.values())
        -min(x["omega"] for x in meshes.values())
    )<5e-9
    assert (
        max(EperN(x) for x in meshes.values())
        -min(EperN(x) for x in meshes.values())
    )<1e-8

    assert primary["BVP_status"]=="SOLVED"
    assert primary["relative_gauss_flux_error"]<5e-5
    assert primary["relative_integrated_stress_defect"]<5e-6
    assert primary["exact_radial_stress_balance_max_residual"]<1e-4
    assert EperN(primary)<base.scalar_mass
    assert EperN(weak)>base.scalar_mass
    assert EperN(stronger_gauge)>base.scalar_mass
    assert high["omega"]<low["omega"]
    assert high["Noether_number"]>low["Noether_number"]
    assert abs(EperN(farther)-EperN(primary))<1e-5
    assert global_U1["canonical_energy"]["electric_inside"]==0

    assert abs(
        conjugate["gauge_charge_integrated"]
        +primary["gauge_charge_integrated"]
    )<1e-8
    assert abs(
        conjugate["A0_at_center"]+primary["A0_at_center"]
    )<1e-8
    assert abs(
        conjugate["canonical_energy"][
            "scalar_plus_electromagnetic_total_including_Coulomb_tail"
        ]-primary["canonical_energy"][
            "scalar_plus_electromagnetic_total_including_Coulomb_tail"
        ]
    )<1e-8

    # Only a widely-separated, leading-order Coulomb estimate.
    # Not an exact two-body or on-board support calculation.
    separation=50.0
    Q=primary["gauge_charge_integrated"]
    interaction=-Q*Q/(4*math.pi*separation)
    pair_force=-Q*Q/(4*math.pi*separation**2)
    assert pair_force<0

    history=archive_status(root)

    return {
        "branch":BRANCH,
        "exact_action_variations":exact,
        "primary_gauged_equilibrium":primary,
        "high_precision_mesh_control":{
            f"n{n}":{
                "omega":v["omega"],
                "E_over_Q":EperN(v),
                "virial_rel":v["relative_integrated_stress_defect"],
                "rms_max":v["BVP_max_collocation_rms"],
            }
            for n,v in meshes.items()
        },
        "larger_domain_control":{
            "radius":farther["spec"]["radius"],
            "omega":farther["omega"],
            "E_over_Q":EperN(farther),
            "gauss_relative_error":
                farther["relative_gauss_flux_error"],
            "tail_relative":farther["tail_f_relative"],
        },
        "local_branch_stability_slope_control":{
            "center_amplitude_low":.68,
            "number_low":low["Noether_number"],
            "omega_low":low["omega"],
            "center_amplitude_high":.72,
            "number_high":high["Noether_number"],
            "omega_high":high["omega"],
            "dQ_domega_finite_difference":(
                (high["Noether_number"]-low["Noether_number"])
                /(high["omega"]-low["omega"])
            ),
            "not_a_proof_of_full_spectral_stability":True,
        },
        "global_U1_no_gauge_control":{
            "number":global_U1["Noether_number"],
            "energy":global_U1["canonical_energy"][
                "scalar_plus_electromagnetic_total_including_Coulomb_tail"
            ],
            "E_over_Q":EperN(global_U1),
        },
        "unbound_branch_negative_control":{
            "center_amplitude":.55,
            "E_over_Q":EperN(weak),
            "classification":"POSITIVE_ENERGY_BUT_NOT_FREE_QUANTUM_BOUND",
        },
        "stronger_gauge_negative_control":{
            "gauge_coupling":.2,
            "E_over_Q":EperN(stronger_gauge),
            "classification":
                "ON_SHELL_BUT_FREE_QUANTUM_ENERGETICALLY_UNBOUND",
        },
        "charge_conjugation":{
            "negative_gauge_charge":
                conjugate["gauge_charge_integrated"],
            "negative_A0_at_center":conjugate["A0_at_center"],
            "same_matter_energy_isolated":primary["canonical_energy"][
                "scalar_plus_electromagnetic_total_including_Coulomb_tail"
            ],
            "isolated_negative_lump_can_be_mirrored":
                "YES_EXACT_CHARGE_CONJUGATION",
            "coupled_two_lump_equilibrium":"NOT_SOLVED",
            "leading_order_Coulomb_pair_at_separation_50":{
                "separation_arbitrary_units":separation,
                "attractive_interaction_energy":interaction,
                "attractive_radial_force":pair_force,
                "exact_composite_self_consistency":"NOT_SOLVED",
            },
        },
        "archival_provenance":history,
        "gates":{
            "P0_PROVENANCE":(
                "PASS" if all(
                    v["status"]=="MATCH" for v in history.values()
                ) else "UNRESOLVED"
            ),
            "P1_SHARED_SCALAR_MAXWELL_ACTION_EOM":
                "PASS_SPHERICALLY_SYMMETRIC_NUMERICAL_BVP",
            "P1_NO_EXTERNAL_TRAP":
                "PASS_FOR_ISOLATED_GAUGED_LUMP",
            "P1_PHI6_UV_COMPLETION":"NOT_DERIVED",
            "P1_Y_PORTAL_VARIATION_AT_FY_ZERO":
                "PASS_ONLY_STATIC_RADIAL_SYMMETRIC_SUBSECTOR",
            "P1_GAUSS_NOETHER_CHARGE":
                "PASS_NUMERICAL_WITH_ANALYTIC_WARD",
            "P1_POSITIVE_ENERGY_WITH_COULOMB_TAIL":
                "PASS_CLASSICAL_SCOPED",
            "P1_INTEGRATED_STRESS_VIRIAL":
                "PASS_WITH_EXTERNAL_COULOMB_TAIL",
            "P1_RADIAL_DYNAMIC_STABILITY":"NOT_CERTIFIED",
            "P1_QUANTUM_UV_AND_NATURALNESS":"NOT_CERTIFIED",
            "P2_TWO_CENTER_ELECTRIC_NEUTRAL_COMPOSITE":
                "NOT_SOLVED",
            "P2_SPINNING_MAGNETIC_Y_SOURCE":"NOT_SOLVED",
            "P2_ISOLATED_SOURCE_GRAVITATIONAL_REPULSION":
                "NOT_DERIVED_POSITIVE_ENERGY_GR_FAR_FIELD_EXPECTED_ATTRACTIVE",
            "P2_FULL_UNIVERSAL_METRIC_CONSTITUTIVE":"NOT_SOLVED",
            "P3_EARTH_DOWN_CRAFT_UP":"NOT_DERIVED",
            "P3_1G_AT_1M_NEUTRAL_MATTER":"NOT_CERTIFIED",
            "B11_M6_FULL_SIGNED_CYCLE":"NOT_RUN",
            "STRICT_COMPLETE_LT10MJ":"NOT_CERTIFIED",
            "006D_REPLACED":"NO",
        },
        "verdict":
            "YELLOW_ISOLATED_GAUGED_SCALAR_SOLITON_ON_SHELL_WITHOUT_COMPOSITE_OR_METRIC_ENGINE",
    }
