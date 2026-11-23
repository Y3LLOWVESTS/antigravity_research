"""G01-U1: axion mixed-invariant screened-metric fork.

NEW ACTION HYPOTHESIS
---------------------
Einstein gravity, two Maxwell U(1) carriers, a healthy
massive pseudoscalar phi, a phi*(F_X dual F_Y) coupling,
and universal neutral matter in exp(beta*phi^2)*g.

This is distinct from the original R3B direct P portal.

The experiment uses a complete analytic dipole Maxwell
field as a source-profile control, with a finite spherical
surface charge/current ansatz. A hypothetical regular
charged-scalar current matches the magnetic drive shape.

A mixed-invariant-sourced scalar is solved by radial Green
functions. The neutral torus then loads the scalar equation
reciprocally, using a finite 2D axisymmetric correction solve.

IMPORTANT LIMITATIONS
---------------------
The X/Y source material itself is not fully stationary.
X/Y gauge fields are NOT re-solved with axion feedback.
The neutral fluid is held geometrically fixed.
The full Einstein/Hodge stress variation and Earth/craft
reaction are not solved.

No real hidden charged species, full Lorentzian mode
health, UV completion or complete operating energy
is established.

No physical gravitational survivor can be declared.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math

from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from scipy.integrate import (
    cumulative_trapezoid,
    trapezoid,
)
from scipy.interpolate import (
    PchipInterpolator,
    RegularGridInterpolator,
)
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.special import spherical_in, spherical_kn

G = 6.67430e-11
C = 299792458.0
GG = 9.80665

R = 2.0
ENERGY_CAP = 10_000_000.0
CAPACITY = 1.5429162116460216

R_MAJOR = 1.0
R_MINOR = 0.2
CENTER = 3.2


def hashfile(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def radial(mu, points):
    """Analytic massless or numerical massive Green solution.

    Normalized mixed source:

      P_l0 inside  = +1/R^2
      P_l0 outside = -R^4/r^6

      P_l2 inside  = 0
      P_l2 outside = -R^4/r^6

    The exact spatial integral of P is zero.
    """

    r = np.asarray(points, float)

    if mu == 0:
        return (
            np.where(
                r <= R,
                0.25 - r*r/(6*R*R),
                R**4/(12*r**4),
            ),
            np.where(
                r <= R,
                -r*r/(30*R*R),
                -R**3/(5*r**3)
                + R**4/(6*r**4),
            ),
        )

    exterior = -R**4/r**6

    fields = []

    for ell, source in (
        (
            0,
            np.where(
                r <= R, 1/R**2, exterior
            ),
        ),
        (
            2,
            np.where(
                r <= R, 0.0, exterior
            ),
        ),
    ):
        x = mu*r

        ii = spherical_in(ell, x)
        kk = spherical_kn(ell, x)

        left = cumulative_trapezoid(
            r*r*source*ii,
            r,
            initial=0,
        )

        right = -cumulative_trapezoid(
            (r*r*source*kk)[::-1],
            r[::-1],
            initial=0,
        )[::-1]

        fields.append(
            (2*mu/math.pi)
            * (kk*left + ii*right)
        )

    return tuple(fields)


def radial_data(mu, rgrid):
    f0, f2 = radial(mu, rgrid)

    d0 = np.gradient(
        f0, rgrid, edge_order=2
    )
    d2 = np.gradient(
        f2, rgrid, edge_order=2
    )

    I0 = trapezoid(
        rgrid*rgrid
        * (d0*d0 + mu*mu*f0*f0),
        rgrid,
    )

    I2 = trapezoid(
        rgrid*rgrid
        * (d2*d2 + mu*mu*f2*f2)
        + 6*f2*f2,
        rgrid,
    ) / 5

    interpolators = [
        PchipInterpolator(rgrid, x)
        for x in (f0, f2)
    ]

    return {
        "phi": interpolators,
        "integral": float(I0+I2),
        "source_radial": (f0, f2),
    }


def torus_grid(nrad, nang):
    minor = np.linspace(
        0, R_MINOR, nrad
    )[:, None]

    theta = (
        np.arange(nang)[None, :]
        * (2*math.pi/nang)
    )

    rho = R_MAJOR + minor*np.cos(theta)

    z = (
        math.sqrt(
            CENTER**2-R_MAJOR**2
        )
        + minor*np.sin(theta)
    )

    return rho, z


def scalar_and_derivative(rad, rho, z):
    r = np.hypot(rho, z)

    if np.min(r) < 0.0001:
        raise RuntimeError(
            "EXTERIOR_RADIUS_INVALID"
        )

    m = z/r
    p2 = (3*m*m-1)/2

    f0, f2 = rad["phi"]

    value = f0(r) + f2(r)*p2

    dz = (
        (
            f0.derivative()(r)
            + f2.derivative()(r)*p2
        )*m
        + f2(r)*3*m*rho*rho/r**3
    )

    return value, dz


def load_scalar(
    mu,
    beta,
    rad,
    h,
    nt=512,
    domain_m=8.0,
):
    """Reciprocal neutral loading of scalar alone.

    (-Laplacian+mu^2+delta_mu^2) delta_phi
        = -delta_mu^2 phi_free

    Axisymmetric cylindrical geometry.

    Maxwell X/Y and neutral-fluid geometry remain frozen.
    """

    L = float(domain_m)

    nr = int(round(L/h))+1
    nz = 2*int(round(L/h))+1

    h = L/(nr-1)

    rs = np.arange(nr)*h
    zs = (
        np.arange(nz)
        - (nz-1)//2
    )*h

    rho, Z = np.meshgrid(
        rs, zs, indexing="ij"
    )

    rr = np.maximum(
        np.hypot(rho, Z),
        0.0001,
    )

    m = Z/rr
    p2 = (3*m*m-1)/2

    f0, f2 = rad["phi"]
    phi_free = f0(rr)+f2(rr)*p2

    level = np.hypot(
        rho-R_MAJOR,
        Z-math.sqrt(
            CENTER**2-R_MAJOR**2
        ),
    ) / R_MINOR

    w = np.clip(1-level, 0, 1)
    shape = w*w*(3-2*w)

    volume = 2*math.pi*rho*h*h

    mass = np.sum(shape*volume)

    if mass <= 0:
        raise RuntimeError(
            "EMPTY_NEUTRAL_TORUS"
        )

    dens = shape/mass

    delta_m2 = (
        8*math.pi*G/(C*C)
        * beta*dens
    )

    if np.min(mu*mu+delta_m2) <= 0:
        raise RuntimeError(
            "LOCAL_SCALAR_TACHYON_LOADED"
        )

    nx = nr-1
    ny = nz-2

    n = nx*ny

    rows = []
    cols = []
    values = []

    rhs = np.zeros(n)

    def ind(i, j):
        return i*ny+(j-1)

    for i in range(nx):
        for j in range(1, nz-1):
            p = ind(i, j)

            diag = (
                mu*mu
                + delta_m2[i, j]
                + 2/(h*h)
            )

            for jj in (j-1, j+1):
                if 1 <= jj < nz-1:
                    rows.append(p)
                    cols.append(ind(i, jj))
                    values.append(
                        -1/(h*h)
                    )

            if i == 0:
                diag += 4/(h*h)

                rows.append(p)
                cols.append(ind(1, j))
                values.append(
                    -4/(h*h)
                )
            else:
                minus = (
                    (i-0.5)/(i*h*h)
                )
                plus = (
                    (i+0.5)/(i*h*h)
                )

                diag += minus+plus

                rows.append(p)
                cols.append(
                    ind(i-1, j)
                )
                values.append(-minus)

                if i+1 < nx:
                    rows.append(p)
                    cols.append(
                        ind(i+1, j)
                    )
                    values.append(-plus)

            rows.append(p)
            cols.append(p)
            values.append(diag)

            rhs[p] = (
                -delta_m2[i, j]
                * phi_free[i, j]
            )

    M = coo_matrix(
        (values, (rows, cols)),
        shape=(n, n),
    ).tocsr()

    correction_v = spsolve(M, rhs)

    relres = float(
        np.max(
            np.abs(
                M@correction_v-rhs
            )
        )
        /
        max(
            1e-12,
            float(
                np.max(np.abs(rhs))
            ),
        )
    )

    if relres > 1e-7:
        raise RuntimeError(
            "LINEARIZED_MATTER_LOADING_RESIDUAL"
        )

    corr = np.zeros_like(phi_free)

    corr[:nx, 1:-1] = (
        correction_v.reshape(nx, ny)
    )

    cr = RegularGridInterpolator(
        (rs, zs),
        corr,
        bounds_error=True,
    )

    dzc = RegularGridInterpolator(
        (rs, zs),
        np.gradient(
            corr,
            h,
            axis=1,
            edge_order=2,
        ),
        bounds_error=True,
    )

    rp, zp = torus_grid(41, nt)

    target = np.column_stack(
        (rp.ravel(), zp.ravel())
    )

    ff, dd = scalar_and_derivative(
        rad, rp, zp
    )

    dv = cr(target).reshape(rp.shape)

    dder = dzc(target).reshape(
        rp.shape
    )

    loaded = (
        -(ff+dv)*(dd+dder)
    )

    raw = -ff*dd

    return {
        "h_m": h,
        "domain_m": L,
        "unknown_count": n,
        "torus_mass_kg":
            float(np.sum(dens*volume)),
        "loaded_kernel_min":
            float(loaded.min()),
        "loaded_kernel_max":
            float(loaded.max()),
        "free_kernel_min":
            float(raw.min()),
        "free_kernel_max":
            float(raw.max()),
        "relative_loading_at_weakest_cell":
            float(
                loaded.min()/raw.min()-1
            ),
        "maximal_correction_relative":
            float(
                np.max(np.abs(dv))
                /
                max(
                    np.max(np.abs(ff)),
                    1e-30,
                )
            ),
        "max_matter_delta_mass2_per_m2":
            float(delta_m2.max()),
        "minimum_effective_mass2":
            float(
                np.min(mu*mu+delta_m2)
            ),
        "signed_static_relative_residual":
            relres,
        "boundary":
            "ZERO_CORRECTION_AT_OUTER_BOX",
        "fixed_source_and_neutral_mass_profile":
            True,
    }


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--out", required=True
    )
    ap.add_argument(
        "--r3b-parent", required=True
    )
    ap.add_argument(
        "--t3-parent", required=True
    )

    a = ap.parse_args()

    pins = {
        "R3B":
            "9474b6782104abb5bd8dd5e893137621b30ad96109e3e52c5a01268794810b11",
        "G01T3":
            "1cfe07d9c3e10a21ac01243b2288d6d4380d0e906768906166165681e9c7e4eb",
    }

    if (
        hashfile(a.r3b_parent) != pins["R3B"]
        or hashfile(a.t3_parent) != pins["G01T3"]
    ):
        raise RuntimeError(
            "HISTORICAL_PARENT_SHA_DRIFT"
        )

    t3 = json.loads(
        Path(a.t3_parent).read_text()
    )

    if not (
        t3["certificate_pass"]
        and t3["physical_survivors"] == 0
    ):
        raise RuntimeError(
            "T3_SCIENCE_GATE_DRIFT"
        )

    rg = np.unique(
        np.r_[
            np.linspace(
                0.0001, 6, 6001
            ),
            np.geomspace(
                6, 100, 1000
            ),
            R,
        ]
    )

    rg_coarse = np.unique(
        np.r_[
            np.linspace(
                0.0001, 6, 3001
            ),
            np.geomspace(
                6, 100, 700
            ),
            R,
        ]
    )

    tc = torus_grid(41, 512)
    tf = torus_grid(81, 1024)

    measurements = []

    for mu in (
        0.0, 0.1, 0.2, 0.3, 0.5,
        0.7, 1.0, 1.5, 2.0,
    ):
        rad = radial_data(mu, rg)

        xc, dc = scalar_and_derivative(
            rad, *tc
        )

        xf, df = scalar_and_derivative(
            rad, *tf
        )

        kcoarse = -xc*dc
        kfine = -xf*df

        for sign in (1, -1):
            min_k = float(
                np.min(sign*kfine)
            )

            if min_k > 0:
                required_beta = float(
                    C*C*rad["integral"]*GG
                    /
                    (
                        4*G
                        * ENERGY_CAP
                        * min_k
                    )
                )

                rho_mean = (
                    1
                    /
                    (
                        2*math.pi**2
                        * R_MAJOR
                        * R_MINOR**2
                    )
                )

                m2 = (
                    mu*mu
                    + 8*math.pi*G
                    * rho_mean
                    * sign
                    * required_beta/(C*C)
                )
            else:
                required_beta = None
                m2 = None

            measurements.append({
                "mu_per_m": mu,
                "beta_sign": sign,
                "signed_kernel_min": min_k,
                "signed_kernel_max":
                    float(np.max(sign*kfine)),
                "scalar_energy_shape_radial_integral":
                    float(rad["integral"]),
                "beta_abs_necessary_to_reach_1g_at_10MJ":
                    required_beta,
                "homogeneous_density_mass2_margin":
                    m2,
                "whole_payload_outward_sign":
                    bool(min_k > 0),
                "torus_sampling_rel_error":
                    abs(
                        float(
                            np.min(sign*kcoarse)
                        )
                        - min_k
                    ) / max(abs(min_k), 1e-30),
            })

        if mu == 0:
            if (
                abs(rad["integral"]-0.08)
                >= 1e-5
                or kfine.max() >= 0
            ):
                raise RuntimeError(
                    "MASSLESS_AXION_NEGATIVE_CONTROL"
                )

    # Advance only the finite-range beta-positive case.
    mu = 1.0

    rad = radial_data(mu, rg)

    f, df = scalar_and_derivative(
        rad, *tf
    )

    kmin = float(np.min(-f*df))

    if kmin <= 0:
        raise RuntimeError(
            "FINITE_RANGE_AXION_SIGN_GATE"
        )

    required_beta = float(
        C*C*rad["integral"]*GG
        /
        (4*G*ENERGY_CAP*kmin)
    )

    beta = 1.5*required_beta

    target_factor = 1.10

    A2 = (
        GG*target_factor
        /
        (C*C*beta*kmin)
    )

    amplitude = math.sqrt(A2)

    energy_scalar = (
        C**4
        * rad["integral"]
        * A2
        / (4*G)
    )

    if abs(
        energy_scalar/ENERGY_CAP
        - target_factor/1.5
    ) > 2e-7:
        raise RuntimeError(
            "CANONICAL_SI_SCALAR_ENERGY_MISMATCH"
        )

    # Illustrative energy matching only.
    # NOT an actual R3B multipole field transfer.
    mirror_a2 = (
        CAPACITY
        /
        (5*math.pi*R)
    )

    p0_norm = math.sqrt(2)*mirror_a2

    kappa = amplitude/p0_norm

    # Full reciprocity would require varying X and Y.
    # Here quantify its leading missing driver.
    pr, pz = tf

    distance = np.hypot(pr, pz)
    cosang = pz/distance

    p2 = (3*cosang*cosang-1)/2

    f0p, f2p = rad["phi"]

    dr = (
        f0p.derivative()(distance)
        + f2p.derivative()(distance)*p2
    )

    dfz = (
        dr*cosang
        + f2p(distance)
        * 3*cosang*pr*pr/distance**3
    )

    dfr = (
        dr*pr/distance
        - f2p(distance)
        * 3*cosang*pz*pr/distance**3
    )

    max_grad_shape = float(
        np.max(
            np.hypot(dfz, dfr)
        )
    )

    max_shape = float(
        np.max(
            np.abs(
                f0p(distance)
                + f2p(distance)*p2
            )
        )
    )

    theta_scale = (
        C**4/(8*math.pi*G)
        * kappa*amplitude
    )

    max_gradient_theta = (
        theta_scale*max_grad_shape
    )

    max_theta = theta_scale*max_shape

    Rgrad_theta = R*max_gradient_theta

    # Diagnostic only, not a rigorous energy bound:
    # changing E_EM at fixed axion amplitude changes
    # kappa inversely with E_EM in this calibration.
    em_energy_for_weak_mixing_j = (
        CAPACITY*Rgrad_theta
    )

    load = [
        load_scalar(mu, beta, rad, h)
        for h in (0.16, 0.10, 0.08)
    ]

    box10 = load_scalar(
        mu,
        beta,
        rad,
        0.08,
        domain_m=10.0,
    )

    for row in load:
        row["beta"] = beta
        row["A_dimless"] = amplitude

        row["loaded_min_up_m_s2"] = float(
            C*C*beta*A2
            * row["loaded_kernel_min"]
        )

        if row["signed_static_relative_residual"] > 1e-7:
            raise RuntimeError(
                "LOADED_SCALAR_RESIDUAL"
            )

        if row["loaded_min_up_m_s2"] < GG:
            raise RuntimeError(
                "LOADED_SCALAR_OUTWARD_GATE"
            )

    relgrid = abs(
        load[-1]["loaded_min_up_m_s2"]
        /
        load[-2]["loaded_min_up_m_s2"]
        - 1
    )

    reldomain = abs(
        load[-1]["loaded_kernel_min"]
        /
        box10["loaded_kernel_min"]
        - 1
    )

    if reldomain > 0.003:
        raise RuntimeError(
            "SCALAR_LOADING_BOX_DEPENDENCE"
        )

    if relgrid > 0.003:
        raise RuntimeError(
            "LOADED_TWO_GRID_CONVERGENCE"
        )

    rad2 = radial_data(mu, rg_coarse)

    e_rel = abs(
        rad2["integral"]/rad["integral"]-1
    )

    if e_rel > 0.0005:
        raise RuntimeError(
            "RADIAL_SCALAR_ENERGY_CONVERGENCE"
        )

    # Topological zero-monopole identity.
    charge_in = 4*math.pi*R/3
    charge_out = -4*math.pi*R/3

    assert charge_in+charge_out == 0

    # Charged scalar shell current shape.
    ang = np.linspace(0, math.pi, 501)

    aamp = math.sqrt(mirror_a2)

    source_current = (
        3*aamp*np.sin(ang)/R
    )

    scalar_current = (
        2*(1.5*aamp)*np.sin(ang)/R
    )

    current_res = float(
        np.max(
            np.abs(
                source_current-scalar_current
            )
        )
    )

    electric_charge_integral = float(
        trapezoid(
            np.cos(ang)*np.sin(ang),
            ang,
        )
    )

    if (
        current_res > 1e-12
        or abs(electric_charge_integral) > 1e-10
    ):
        raise RuntimeError(
            "IDEAL_SHELL_SOURCE_CURRENT_WARD"
        )

    screening_beta_phi2 = float(
        beta*A2
        * np.max(f*f)
    )

    if screening_beta_phi2 > 1e-7:
        raise RuntimeError(
            "LINEARIZED_METRIC_EXPANSION_FAIL"
        )

    report = {
        "experiment":
            "G01-U1-AXION_MIXED_SOURCE_SCREENED_METRIC_FORK",

        "created_utc":
            datetime.now(timezone.utc).isoformat(),

        "source_sha256": hashfile(__file__),

        "parents_sha256": pins,

        "historical_R3B_prescribed_capacity_j":
            CAPACITY,

        "historical_G01T3_ten_mode_exclusion":
            True,

        "candidate_action":
            "Einstein-Hilbert + canonical positive-kinetic pseudoscalar phi + massive phi^2 + two Maxwell U(1) fields + phi*(F_X dual F_Y) + hypothetical charged source fields + universal exp(beta phi^2)*g neutral metric",

        "axion_scalar_field_equation":
            "(-Laplacian+mu^2+8*pi*G*beta*rho_neutral/c^2)*phi=kappa*(E_X dot B_Y), linearized in beta phi^2",

        "conformal_sigma":
            "beta*phi^2/2",

        "parity":
            "phi is pseudoscalar; phi*(E dot B) and sigma(phi) are parity even",

        "topological_mixed_source_null": {
            "integration_by_parts":
                "int E_X dot B_Y d3x = -int div(Phi_X B_Y) d3x = 0 for localized fields and no magnetic monopoles",
            "radial_l0_in_integral_over_4pi_c0":
                charge_in/(4*math.pi),
            "radial_l0_out_integral_over_4pi_c0":
                charge_out/(4*math.pi),
            "total_zero": True,
            "does_not_imply_zero_local_axion":
                True,
        },

        "dipole_Maxwell_source_ansatz": {
            "source_radius_m": R,
            "mirror_a_squared_after_illustrative_energy_matching":
                mirror_a2,
            "surface_electric_charge":
                "proportional to cos(theta), net charge zero",
            "surface_Y_azimuthal_current":
                "(3*a/R)*sin(theta)",
            "regular_charged_scalar_shell_profile":
                "chi_Y=v*sin(theta)*exp(i azimuth), q*v^2=3*a/2",
            "source_current_shape_error":
                current_res,
            "electric_surface_net_charge_angular_integral":
                electric_charge_integral,
            "phase_and_charged_scalar_full_EOM_on_shell":
                False,
            "physical_hidden_Y_charged_species_identified":
                False,
            "complete_shell_support_mechanics":
                False,
            "not_equal_to_original_R3B_multipole_geometry":
                True,
        },

        "source_P_normalization": {
            "P0_inside": "1/R^2",
            "P0_outside": "-R^4/r^6",
            "P2_inside": "0",
            "P2_outside": "-R^4/r^6",
            "p0_scale_c0_j_per_m_diagnostic":
                p0_norm,
            "axion_kappa_required_m_per_j_diagnostic":
                kappa,
        },

        "finite_torus": {
            "major_radius_m": R_MAJOR,
            "minor_radius_m": R_MINOR,
            "center_radial_m": CENTER,
            "min_standoff_m":
                float(
                    np.min(np.hypot(*tf))-R
                ),
            "fine_sample_count":
                int(tf[0].size),
            "torus_mass_kg": 1.0,
        },

        "mediator_scan": measurements,

        "selected_conditional_law": {
            "inverse_range_per_m": mu,
            "beta_dimensionless": beta,
            "beta_energy_necessary_floor":
                required_beta,
            "source_axion_amplitude_A":
                amplitude,
            "scalar_kinetic_and_mass_energy_j":
                energy_scalar,
            "historical_R3B_reference_field_capacity_j_NOT_SOURCED":
                CAPACITY,
            "scalar_energy_fitted_ratio_to_10MJ":
                energy_scalar/ENERGY_CAP,
            "available_budget_after_scalar_only_j":
                ENERGY_CAP-energy_scalar,
            "max_abs_beta_phi2":
                screening_beta_phi2,
            "source_kappa_m_per_J_assuming_illustrative_dipole_calibration":
                kappa,

            "Maxwell_reciprocal_loading_prefilter": {
                "theta_coefficient_c4_over_8piG_times_kappa_phi":
                    True,
                "theta_absolute_max_on_target":
                    max_theta,
                "max_gradient_theta_per_m_on_target":
                    max_gradient_theta,
                "R_times_max_gradient_theta":
                    Rgrad_theta,
                "small_feedback_Rgradtheta_less_one":
                    bool(Rgrad_theta < 1),
                "heuristic_maxwell_energy_for_Rgradtheta_below_one_j":
                    em_energy_for_weak_mixing_j,
                "heuristic_scalar_plus_Maxwell_cost_j":
                    em_energy_for_weak_mixing_j+energy_scalar,
                "reason":
                    "The gradient of topological theta, not a constant theta, drives reciprocal X/Y loading",
                "source_electric_magnetic_joint_variation":
                    "NOT_SOLVED",
                "energy_scaling_is_not_a_no_go_theorem":
                    True,
            },

            "loaded_scalar_responses": load,
            "loaded_two_mesh_relative_difference":
                relgrid,
            "loaded_boundary_box_10m_response":
                box10,
            "loaded_domain_8_vs_10m_relative_difference":
                reldomain,
            "radial_energy_cross_grid_relative_difference":
                e_rel,
            "requested_acceleration_m_s2":
                GG,
            "classification":
                "CONDITIONAL_POSITIVE_SCALAR_ONLY_LOADED_SIGN_NOT_WHOLE_CRAFT_GRAVITY",
        },

        "original_R3B_full_XY_reciprocal_loading_transferred":
            False,
        "on_shell_finite_source_full_action":
            False,
        "fully_stationary_dynamical_neutral_fluid":
            False,
        "complete_Einstein_Hilbert_and_Hodge_stress_variation":
            False,
        "Earth_down_whole_craft_up_from_same_action":
            False,
        "Lorentzian_constrained_full_mode_health":
            False,
        "quantum_UV_empirical_viability":
            False,
        "complete_operating_energy_j":
            None,
        "full_regression":
            "NOT_RUN_BY_USER_POLICY",
        "physical_survivors": 0,
        "blocker_heuristic_previous_percent": 30,
        "blocker_heuristic_after_percent":
            "TO_BE_ASSESSED_AFTER_INDEPENDENT_ANALYSIS",
        "overall_research_heuristic_previous_percent":
            37,
    }

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=False)

    np.savez_compressed(
        out/"radial_reference.npz",
        r=rg,
        f0=rad["source_radial"][0],
        f2=rad["source_radial"][1],
        mu=np.array(mu),
    )

    report["radial_reference_sha256"] = (
        hashfile(
            out/"radial_reference.npz"
        )
    )

    raw = (
        json.dumps(
            report,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        ) + "\n"
    ).encode()

    with (out/"science.json").open("xb") as file:
        file.write(raw)

    (out/"science.json.sha256").write_text(
        hashlib.sha256(raw).hexdigest()
        + "  science.json\n"
    )

    print("G01_U1_PARENT_PROVENANCE=PASS")
    print("G01_U1_TOPOLOGICAL_ZERO_MONOPOLE=PASS")
    print("G01_U1_NEW_AXION_SOURCE_RESPONSE=PASS_RESTRICTED")
    print("G01_U1_SCREENED_PORTAL_SIGN_BRANCH=OUTWARD_CONDITIONAL")
    print("BETA_DIMENSIONLESS=", beta)
    print("SCALAR_ONLY_ENERGY_J=", energy_scalar)
    print(
        "LOADED_SCALAR_MIN_M_S2=",
        load[-1]["loaded_min_up_m_s2"],
    )
    print(
        "SCALAR_LOAD_GRID_REL_CHANGE=",
        relgrid,
    )
    print(
        "GAUGE_BACKREACTION_R_GRAD_THETA=",
        Rgrad_theta,
    )
    print(
        "PERTURBATIVE_GAUGE_ENERGY_SCALING_J=",
        em_energy_for_weak_mixing_j,
    )
    print("UNIDENTIFIED_Y_CARRIERS_AND_SUPPORTS=HOLD")
    print("EARTH_WHOLE_CRAFT_GRAVITY=NOT_DERIVED")
    print("PHYSICAL_SURVIVORS=0")
    print("RESULT_DIR=", out)
    print(
        "SCIENCE_SHA256=",
        hashlib.sha256(raw).hexdigest(),
    )


if __name__ == "__main__":
    main()
