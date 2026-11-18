"""BETA1-1B1: alpha=0 on-shell Y-channel constrained gradient preflight.

Scientific target
-----------------
Distinguish a negative restricted magnetic-energy curvature (BETA1-1B0)
from a propagating ghost, a Gauss artifact, or an actual negative-square-
frequency Y mode in the same flat-space charged-scalar/X/Y candidate action.

The zero-Y P10 background is stationary within this branch at alpha=0:
    sigma(P) = -beta*P**2
    lambda(P=0) = 0
    delta sigma = O(Y**2)

At first order, Y decouples from X and scalar perturbations.

Quadratic Y Lagrangian:

    L2 = |E_Y|**2/2 - |B_Y|**2/2
         + 2*beta*(G-T+2U)*(E_X dot B_Y)**2

T = sum(f_i**2*W_i**2)
G = sum(|grad f_i|**2)
U = full P10 source potential

The electric Y kinetic term is standard Maxwell and positive.
An axisymmetric azimuthal Y perturbation satisfies the Y Gauss constraint.

Limitations:
    P10 source solutions are discrete, not continuum-certified.
    Full alpha!=0 reciprocal dynamics are NOT tested.
    No complete metric, gravitational, neutral-matter, or craft-force result.
    No SI energy or physical accelerator claim.
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp

from scipy.linalg import eigh

from antigravity_research.beta_artificial.beta1_1b0_p10_local_response import (
    source_arrays,
    vector_potential_basis,
)


CASES = (
    ("coarse12_L12", 12, 12.0),
    ("base18_L12", 18, 12.0),
    ("fixed_h24_L16", 24, 16.0),
    ("fixed_h30_L20", 30, 20.0),
    ("refine36_L16", 36, 16.0),
)


def exact_branch_theorems():
    """Independently differentiate the alpha=0 Lorentzian action."""

    b, ey, ex, beta, T, G, U = sp.symbols(
        "b E_Y E_X beta T G U",
        real=True,
    )

    sigma = -beta*(ex*b)**2

    lag = (
        ey**2/sp.Integer(2)
        - b**2/sp.Integer(2)
        + (T-G)*sp.exp(2*sigma)
        - U*sp.exp(4*sigma)
    )

    d_b = sp.simplify(
        sp.diff(lag, b).subs({
            b: 0,
            ey: 0,
        })
    )

    d2_b = sp.simplify(
        sp.diff(lag, b, 2).subs({
            b: 0,
            ey: 0,
        })
    )

    d2_ey = sp.simplify(
        sp.diff(lag, ey, 2).subs({
            b: 0,
            ey: 0,
        })
    )

    d2_mixed = sp.simplify(
        sp.diff(lag, ey, b).subs({
            b: 0,
            ey: 0,
        })
    )

    kappa = G-T+2*U

    expected = (
        -1
        +4*beta*ex**2*kappa
    )

    p = sp.symbols("p", real=True)

    sig_p = -beta*p*p

    lam = -(
        2*sp.exp(2*sig_p)*(G-T)
        +4*sp.exp(4*sig_p)*U
    )*sp.diff(sig_p, p)

    q, angle = sp.symbols(
        "q theta",
        real=True,
    )

    c2 = (
        1
        -4*beta*kappa*ex**2
        *sp.sin(angle)**2
    )

    omega2 = q*q*c2

    checks = {
        "zero_Y_stationary_alpha0":
            d_b == 0,

        "positive_electric_Y_kinetic":
            d2_ey == 1,

        "electric_magnetic_velocity_cross_null":
            d2_mixed == 0,

        "magnetic_quadratic_action_sign":
            sp.simplify(
                d2_b-expected
            ) == 0,

        "lambda_P0_zero":
            sp.simplify(
                lam.subs(p, 0)
            ) == 0,

        "lambda_linear_response":
            sp.simplify(
                sp.diff(lam, p).subs(p, 0)
                -4*beta*kappa
            ) == 0,

        "beta0_maxwell_characteristic":
            sp.simplify(
                c2.subs(beta, 0)-1
            ) == 0,

        "wave_perp_E_characteristic":
            sp.simplify(
                c2.subs(angle, sp.pi/2)
                -(1-4*beta*kappa*ex**2)
            ) == 0,

        "wave_parallel_E_characteristic":
            sp.simplify(
                c2.subs(angle, 0)-1
            ) == 0,

        "positive_beta_nonnegative_kappa_decreases_stiffness":
            sp.simplify(
                sp.diff(c2, beta)
                +4*kappa*ex**2*sp.sin(angle)**2
            ) == 0,
    }

    if not all(checks.values()):
        raise AssertionError(
            "Exact branch theorem failure: "
            +str(checks)
        )

    return {
        "checks": checks,

        "action_definition":
            "L_Y2=|E_Y|^2/2-|B_Y|^2/2"
            "+2*beta*(G-T+2U)*(E_X.B_Y)^2",

        "magnetic_hessian_parallel":
            str(-d2_b),

        "electric_kinetic_hessian":
            str(d2_ey),

        "lambda_linear_coefficient":
            str(
                sp.diff(lam, p).subs(p, 0)
            ),

        "local_omega_squared":
            str(omega2),

        "branch_is_on_shell_only_for_alpha0":
            True,

        "Gauss_Ward_linearization":
            "Y Gauss: div(E_Y)=0 for BX=0; "
            "X Gauss and scalar/Noether decouple "
            "at first order because lambda0="
            "sigma_prime0=0; axisymmetric Y_phi "
            "is divergence-free",
    }


def basis_matrices(
    model,
    arrays,
    family="legacy",
):
    """Construct independent positive electric mass and magnetic Hessian.

    legacy:
        Reproduce the eight Gaussian modes of BETA1-1B0.

    dirichlet:
        Multiply by a smooth squared boundary envelope.

    B_r = -partial_z A_phi

    B_z = partial_r A_phi + A_phi/r
    """

    if family not in (
        "legacy",
        "dirichlet",
    ):
        raise ValueError("Unknown basis")

    r = model.rho.reshape(
        model.nr,
        model.nz,
    )

    z = model.z.reshape(
        model.nr,
        model.nz,
    )

    h = model.h

    prior_B, specs = vector_potential_basis(
        model
    )

    functions = []
    fields = []

    for rw, zw, center in specs:
        phi = r*np.exp(
            -.5*(
                (r/rw)**2
                +((z-center)/zw)**2
            )
        )

        if family == "dirichlet":
            phi *= (
                (1-(r/model.s.L)**2)**2
                *(1-(z/model.s.L)**2)**2
            )

        Br = -np.gradient(
            phi,
            h,
            axis=1,
            edge_order=2,
        )

        Bz = (
            np.gradient(
                phi,
                h,
                axis=0,
                edge_order=2,
            )
            +phi/r
        )

        functions.append(phi)

        fields.append(
            np.stack(
                (Br, Bz)
            )
        )

    phi = np.asarray(functions)
    B = np.asarray(fields)

    if family == "legacy":
        if not np.allclose(
            B,
            prior_B,
            atol=2e-13,
            rtol=1e-12,
        ):
            raise AssertionError(
                "Frozen BETA1-1B0 basis not reproduced"
            )

    w = model.w
    n = len(specs)

    a = phi.reshape(n, -1)
    bvec = B.reshape(n, 2, -1)

    dot = (
        B[:, 0]*arrays["Er"]
        +B[:, 1]*arrays["Ez"]
    ).reshape(n, -1)

    kappa = (
        arrays["G"]
        -arrays["T"]
        +2*arrays["U"]
    ).ravel()

    kinetic = np.einsum(
        "in,jn,n->ij",
        a,
        a,
        w,
        optimize=True,
    )

    magnetic = np.einsum(
        "icn,jcn,n->ij",
        bvec,
        bvec,
        w,
        optimize=True,
    )

    beta_operator = np.einsum(
        "in,jn,n->ij",
        dot,
        dot,
        4*kappa*w,
        optimize=True,
    )

    kinetic = (
        kinetic+kinetic.T
    )/2

    magnetic = (
        magnetic+magnetic.T
    )/2

    beta_operator = (
        beta_operator+beta_operator.T
    )/2

    if np.linalg.eigvalsh(kinetic)[0] <= 1e-12:
        raise AssertionError(
            "Positive Maxwell mass not established"
        )

    return {
        "kinetic": kinetic,
        "magnetic": magnetic,
        "beta_operator": beta_operator,
        "phi": phi,
        "B": B,
        "basis_size": n,
        "family": family,
    }


def lowest_wave_mode(mats, beta):
    """Solve the gauge-reduced generalized frequency problem.

    (K_B-beta*D) q = omega^2 M_E q
    """

    K = (
        mats["magnetic"]
        -beta*mats["beta_operator"]
    )

    M = mats["kinetic"]

    eig, vec = eigh(
        K,
        M,
        check_finite=True,
    )

    q = vec[:, 0]

    residual = np.linalg.norm(
        K@q-eig[0]*M@q
    )/max(
        1.,
        np.linalg.norm(K@q),
    )

    return {
        "omega_squared_min":
            float(eig[0]),

        "omega_squared_max":
            float(eig[-1]),

        "negative_mode_count":
            int(np.count_nonzero(eig < -1e-9)),

        "max_growth_rate_canonical_inverse_time":
            float(
                math.sqrt(
                    max(0., -eig[0])
                )
            ),

        "eigen_residual":
            float(residual),

        "q": q,
    }


def beta_threshold(mats):
    """Find first fixed-basis zero of omega squared."""

    lo = 0.
    hi = 100.

    if (
        lowest_wave_mode(mats, lo)[
            "omega_squared_min"
        ] <= 0
        or
        lowest_wave_mode(mats, hi)[
            "omega_squared_min"
        ] >= 0
    ):
        raise AssertionError(
            "Critical beta was not bracketed"
        )

    for _ in range(30):
        mid = (lo+hi)/2

        value = lowest_wave_mode(
            mats,
            mid,
        )["omega_squared_min"]

        if value > 0:
            lo = mid
        else:
            hi = mid

    return float(
        (lo+hi)/2
    )


def bianchi_mode_error(
    model,
    mats,
    q,
):
    """Calculate cylindrical magnetic Bianchi residual.

    The Y Gauss result is analytic from axisymmetry:
    div(E_phi e_phi)=(1/r)*partial_phi(E_phi)=0.
    """

    B = np.tensordot(
        q,
        mats["B"],
        axes=(0, 0),
    )

    r = model.rho.reshape(
        model.nr,
        model.nz,
    )

    h = model.h

    dr = lambda x: np.gradient(
        x,
        h,
        axis=0,
        edge_order=2,
    )

    dz = lambda x: np.gradient(
        x,
        h,
        axis=1,
        edge_order=2,
    )

    divergence = (
        dr(B[0])
        +B[0]/r
        +dz(B[1])
    )

    return {
        "Bianchi_magnetic_divergence_inf":
            float(
                np.max(
                    abs(divergence)
                )
            ),

        "Y_Gauss_Ephi_divergence":
            0.,

        "Y_Gauss_kind":
            "ANALYTIC_AXISYMMETRIC_PHI_ONLY",

        "Y_gauge_kind":
            "PHI_COMPONENT_IS_NOT_SINGLE_VALUED_"
            "AXISYMMETRIC_GRADIENT",
    }


def projected_time_evolution(
    mats,
    mode,
    beta,
    final_time=1.25,
    steps=250,
):
    """Independent velocity-Verlet integration with signed energy."""

    M = mats["kinetic"]

    K = (
        mats["magnetic"]
        -beta*mats["beta_operator"]
    )

    eigen = mode["omega_squared_min"]

    if eigen >= 0:
        raise ValueError(
            "Negative omega squared required"
        )

    q0 = mode["q"]

    q = q0.copy()
    vel = np.zeros_like(q)

    dt = final_time/steps

    force = lambda state: -np.linalg.solve(
        M,
        K@state,
    )

    a = force(q)

    energy = lambda x, v: .5*(
        v@M@v+x@K@x
    )

    e0 = energy(q, vel)

    for _ in range(steps):
        q = (
            q
            +dt*vel
            +.5*dt*dt*a
        )

        nxt = force(q)

        vel = (
            vel
            +.5*dt*(a+nxt)
        )

        a = nxt

    predicted = math.cosh(
        math.sqrt(-eigen)*final_time
    )

    measured = float(
        q@M@q0/(q0@M@q0)
    )

    final_energy = energy(
        q,
        vel,
    )

    return {
        "time_canonical":
            final_time,

        "steps":
            steps,

        "predicted_mode_amplification":
            predicted,

        "computed_mode_amplification":
            measured,

        "amplitude_relative_error":
            abs(measured-predicted)/predicted,

        "initial_projected_energy":
            float(e0),

        "final_projected_energy":
            float(final_energy),

        "energy_ledger_absolute_error":
            abs(final_energy-e0),

        "criterion":
            "DISCRETE_LINEARIZED_RESTRICTED_"
            "Y_GALERKIN_ONLY",
    }


def single_case(nr, L, prior=None):
    """Calculate one reconstructed source and both mode families."""

    model, info, arrays = source_arrays(
        nr,
        L,
    )

    kappa = (
        arrays["G"]
        -arrays["T"]
        +2*arrays["U"]
    )

    slope = (
        4*kappa*arrays["E2"]
    )

    if np.min(kappa) < -1e-9:
        raise AssertionError(
            "Kappa sign changed: monotonic beta "
            "argument no longer valid"
        )

    local = {}

    for beta in (
        0., 40., 50.,
        60., 75., 100.,
    ):
        c2 = (
            1-beta*slope
        )

        core = c2[
            2:-2,
            3:-3,
        ]

        local[str(int(beta))] = {
            "min_c_squared":
                float(np.min(c2)),

            "interior_min_c_squared":
                float(np.min(core)),

            "negative_cell_fraction":
                float(np.mean(c2 < 0)),

            "interior_negative_cell_fraction":
                float(np.mean(core < 0)),

            "max_gamma_over_k_parallel_E_perp_k":
                float(
                    math.sqrt(
                        max(0., -np.min(c2))
                    )
                ),
        }

    result = {
        "nr": nr,

        "L_canonical": L,

        "h_canonical": model.h,

        "source_eom_L2":
            info["scalar_equation_weighted_L2"],

        "source_charge":
            info["net_X_charge"],

        "source_energy_CANONICAL_NOT_J":
            info["canonical_energy_NOT_J"],

        "Y_current_alpha0":
            info["Y_first_order_alpha0_current_L2"],

        "Y_current_alpha1_OFF_SHELL_ZERO_Y_REFERENCE":
            info["Y_first_order_alpha1_current_L2"],

        "Kappa_min":
            float(np.min(kappa)),

        "local_threshold_beta_alpha0":
            float(1./max(slope.ravel())),

        "local_principal":
            local,

        "basis": {},
    }

    for family in (
        "legacy",
        "dirichlet",
    ):
        mats = basis_matrices(
            model,
            arrays,
            family,
        )

        spectra = {
            str(int(beta)):
                lowest_wave_mode(mats, beta)
            for beta in (
                0., 40., 50.,
                60., 75., 100.,
            )
        }

        critical = beta_threshold(mats)

        observed = spectra["100"]

        ward = bianchi_mode_error(
            model,
            mats,
            observed["q"],
        )

        temporal = projected_time_evolution(
            mats,
            observed,
            100.,
        )

        if (
            family == "legacy"
            and prior is not None
        ):
            reference = prior[
                "alpha0_Ritz_beta_critical_fixed_basis"
            ]

            if abs(reference-critical) > 2e-3:
                raise AssertionError(
                    "BETA1-1B0 threshold drift: "
                    f"{critical} vs {reference}"
                )

            reference_eig = prior[
                "rayleigh_alpha0_beta100"
            ]["minimum"]

        else:
            reference = None
            reference_eig = None

        result["basis"][family] = {
            "kinetic_matrix_min_eigenvalue":
                float(
                    np.min(
                        np.linalg.eigvalsh(
                            mats["kinetic"]
                        )
                    )
                ),

            "kinetic_matrix_condition_number":
                float(
                    np.linalg.cond(
                        mats["kinetic"]
                    )
                ),

            "critical_beta":
                critical,

            "previous_static_Ritz_critical_beta":
                reference,

            "previous_static_Ritz_min_beta100":
                reference_eig,

            "spectrum": {
                key: {
                    k: v
                    for k, v in mode.items()
                    if k != "q"
                }
                for key, mode in spectra.items()
            },

            "constraints":
                ward,

            "time_evolution":
                temporal,

            "support":
                (
                    "GAUSSIAN_AXIS_REGULAR;"
                    "SMOOTH_BOUNDARY_TAPER"
                    if family == "dirichlet"
                    else "FROZEN_LEGACY_GAUSSIAN"
                ),
        }

    if not (
        max(result["source_eom_L2"]) < 1e-4
        and abs(result["source_charge"]) < 1e-7
    ):
        raise AssertionError(
            "No longer matching P10 source"
        )

    return result


def run_cases(previous_cases):
    """Reconstruct five P10 backgrounds and test both Y bases."""

    symbolic = exact_branch_theorems()
    result = {}

    for name, nr, L in CASES:
        if name not in previous_cases:
            raise AssertionError(
                "Frozen BETA1-1B0 case missing"
            )

        result[name] = single_case(
            nr,
            L,
            previous_cases[name],
        )

    gate = {
        "symbolic_action_gauge_checks":
            all(symbolic["checks"].values()),

        "source_gauss_eom_all":
            all(
                max(c["source_eom_L2"]) < 1e-4
                and abs(c["source_charge"]) < 1e-7
                for c in result.values()
            ),

        "zero_alpha_Y_null":
            all(
                c["Y_current_alpha0"] < 1e-13
                for c in result.values()
            ),

        "Kappa_nonnegative_sampled":
            all(
                c["Kappa_min"] >= -1e-9
                for c in result.values()
            ),

        "beta0_local_positive":
            all(
                c["local_principal"]["0"][
                    "min_c_squared"
                ] > 0
                for c in result.values()
            ),

        "beta50_local_positive":
            all(
                c["local_principal"]["50"][
                    "min_c_squared"
                ] > 0
                for c in result.values()
            ),

        "beta100_local_negative":
            all(
                c["local_principal"]["100"][
                    "min_c_squared"
                ] < -.2
                for c in result.values()
            ),

        "beta100_interior_negative":
            all(
                c["local_principal"]["100"][
                    "interior_min_c_squared"
                ] < 0
                for c in result.values()
            ),

        "alpha0_electric_kinetic_positive":
            all(
                f["kinetic_matrix_min_eigenvalue"] > 0
                for c in result.values()
                for f in c["basis"].values()
            ),

        "beta0_dynamic_positive":
            all(
                f["spectrum"]["0"][
                    "omega_squared_min"
                ] > 0
                for c in result.values()
                for f in c["basis"].values()
            ),

        "beta50_dynamic_positive":
            all(
                f["spectrum"]["50"][
                    "omega_squared_min"
                ] > 0
                for c in result.values()
                for f in c["basis"].values()
            ),

        "beta75_dynamic_negative":
            all(
                f["spectrum"]["75"][
                    "omega_squared_min"
                ] < 0
                for c in result.values()
                for f in c["basis"].values()
            ),

        "beta100_dynamic_negative":
            all(
                f["spectrum"]["100"][
                    "omega_squared_min"
                ] < -.05
                for c in result.values()
                for f in c["basis"].values()
            ),

        "both_bases_negative":
            all(
                all(
                    c["basis"][key]["spectrum"]["100"][
                        "negative_mode_count"
                    ] > 0
                    for key in (
                        "legacy",
                        "dirichlet",
                    )
                )
                for c in result.values()
            ),

        "constraints_and_Bianchi":
            all(
                f["constraints"][
                    "Bianchi_magnetic_divergence_inf"
                ] < 2e-11
                and f["constraints"][
                    "Y_Gauss_Ephi_divergence"
                ] == 0
                for c in result.values()
                for f in c["basis"].values()
            ),

        "eigen_residual_small":
            all(
                f["spectrum"]["100"][
                    "eigen_residual"
                ] < 1e-9
                for c in result.values()
                for f in c["basis"].values()
            ),

        "time_domain_growth_reproduced":
            all(
                f["time_evolution"][
                    "computed_mode_amplification"
                ] > 1.05
                and f["time_evolution"][
                    "amplitude_relative_error"
                ] < 1e-4
                for c in result.values()
                for f in c["basis"].values()
            ),

        "time_domain_energy_ledger":
            all(
                f["time_evolution"][
                    "energy_ledger_absolute_error"
                ] < 1e-3
                for c in result.values()
                for f in c["basis"].values()
            ),

        "parent_static_Ritz_threshold_consistent":
            all(
                abs(
                    c["basis"]["legacy"][
                        "critical_beta"
                    ]
                    -c["basis"]["legacy"][
                        "previous_static_Ritz_critical_beta"
                    ]
                ) < 2e-3
                for c in result.values()
            ),

        "fixed_h_domain_growth_convergence":
            abs(
                result["fixed_h24_L16"]["basis"][
                    "dirichlet"
                ]["spectrum"]["100"]["omega_squared_min"]
                -result["fixed_h30_L20"]["basis"][
                    "dirichlet"
                ]["spectrum"]["100"]["omega_squared_min"]
            ) < .08,

        "mesh_refinement_growth_consistency":
            abs(
                result["fixed_h24_L16"]["basis"][
                    "dirichlet"
                ]["spectrum"]["100"]["omega_squared_min"]
                -result["refine36_L16"]["basis"][
                    "dirichlet"
                ]["spectrum"]["100"]["omega_squared_min"]
            ) < .4,
    }

    return {
        "symbolic": symbolic,
        "cases": result,
        "gates": gate,

        "classification":
            "ACTION_DERIVED_RESTRICTED_"
            "LINEAR_DYNAMIC_OBSTRUCTION",

        "verdict":
            "YELLOW_ALPHA0_CONSTRAINED_Y_GRADIENT_"
            "INSTABILITY_BETA100_NONZERO_ALPHA_OPEN",

        "gauge_conclusion":
            "POSITIVE_MAXWELL_Y_TIME_KINETIC_"
            "NO_Y_GHOST_IN_TESTED_ALPHA0_CHANNEL;"
            "NEGATIVE_OMEGA_SQUARED_GRADIENT_MODE",

        "stationarity":
            "ALPHA0_Y0_IS_STATIONARY_IN_FLAT_SOURCE_ONLY_ACTION;"
            "ALPHA_NONZERO_Y0_IS_NOT_THE_INDUCED_SOLUTION",

        "physical_transfer":
            "NOT_AUTHORIZED",

        "limitations": [
            "Flat space, alpha=0, Y=0; beta=100 is "
            "hypothetical canonical, not a physical operating point",

            "P10 finite-grid stationary source; no rigorous "
            "continuum convergence or exact UV completion",

            "Eight-function Gaussian/Dirichlet azimuthal "
            "Galerkin space is not the entire constrained spectrum",

            "Pointwise plane-wave principal symbol is "
            "a frozen-coefficient local approximation",

            "Neutral Earth/support trace can modify portal "
            "curvature; complete universal metric/stress absent",

            "No full nonzero-alpha reciprocal stationary "
            "source/X/Y or coupled gauge/phase spectrum",

            "No sourced neutral 1kg payload acceleration, "
            "Earth-down/craft-up, SI energy, or whole craft lift",
        ],

        "next":
            "BETA1-02 passive material reciprocity/C2;"
            "then nonzero-alpha on-shell reciprocal source/Y",
    }
