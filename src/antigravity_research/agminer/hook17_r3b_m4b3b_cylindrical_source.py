"""B17-M4B3B: 2-D conservative B7 charge deposition preflight.

Map the B7 electric source into the axisymmetric (z,rho) scalar
nodes used by the existing R3X1 carrier operator.

Integrate the original 10 cm shell in spherical (r,mu) coordinates,
including its 2*pi azimuthal measure. A compact bilinear transfer
keeps all source nodes within the onboard radius and conserves total
quadrature charge.

This is GLOBAL charge-conserving nodal deposition, NOT exact local
finite-volume integration over cylindrical cells.

Neither global neutrality nor radial moment conservation proves
higher-multipole fidelity after two-dimensional deposition.

This run does not certify loaded response, source hardware, complete
energy, whole-craft force or a physical antigravity mechanism.
"""

from __future__ import annotations

import math
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import eval_legendre

from .hook17_fdual_f_r3x3b7_finite_charge_shell import (
    source_density_proxy,
)

BRANCH = "032H17A12D1R3X3B17-M4B3B"


def deposit_b7_to_axisymmetric_nodes(
    zs,
    rhos,
    h,
    amplitudes,
    *,
    source_radius_m=2.0,
    shell_width_m=0.10,
    radial_order=48,
    angular_order=96,
):
    """Construct a source RHS on the existing scalar-potential nodes.

    Nodes correspond to [1:-1, :-1] on the full (z,rho) grid.
    The scalar-axis dual-volume weight uses rho=h/8 at rho=0,
    matching the established R3X1 discretization.

    Every quadrature charge is distributed across nearby eligible
    onboard nodes using normalized bilinear weights.
    """

    zs = np.asarray(zs, dtype=float)
    rhos = np.asarray(rhos, dtype=float)
    amps = np.asarray(amplitudes, dtype=float)

    if (
        zs.ndim != 1
        or rhos.ndim != 1
        or len(zs) < 8
        or len(rhos) < 8
        or amps.ndim != 1
        or not amps.size
        or not np.isfinite(amps).all()
        or not np.isfinite(zs).all()
        or not np.isfinite(rhos).all()
        or not np.isfinite(h)
        or h <= 0
        or not 0 < shell_width_m < source_radius_m
        or abs(rhos[0]) > 1e-12
        or not np.allclose(np.diff(zs), h, rtol=1e-8, atol=1e-10)
        or not np.allclose(np.diff(rhos), h, rtol=1e-8, atol=1e-10)
        or type(radial_order) is not int
        or radial_order < 12
        or type(angular_order) is not int
        or angular_order < max(32, 2 * len(amps) + 4)
    ):
        raise ValueError("Invalid B7 source deposition inputs")

    xr, wr = leggauss(radial_order)
    mu, wmu = leggauss(angular_order)

    radii = (
        source_radius_m
        - 0.5 * shell_width_m
        + 0.5 * shell_width_m * xr
    )
    wr = wr * shell_width_m / 2

    profile = np.zeros(
        (radial_order, angular_order), dtype=float
    )

    for ell, amplitude in enumerate(amps, start=1):
        if amplitude:
            q = source_density_proxy(
                ell,
                float(amplitude),
                source_radius_m,
                shell_width_m,
                radii,
            )
            profile += (
                q[:, None]
                * eval_legendre(ell, mu)[None, :]
            )

    qnodes = np.zeros(
        (len(zs) - 2, len(rhos) - 1),
        dtype=float,
    )

    max_spread = 0.0
    truncated = 0
    original_charge = 0.0
    original_abs_charge = 0.0

    for ir, rad in enumerate(radii):
        for im, u in enumerate(mu):
            z = float(rad * u)
            rho = float(
                rad * math.sqrt(max(0.0, 1.0 - u*u))
            )

            dq = float(
                2 * math.pi * rad*rad
                * wr[ir] * wmu[im]
                * profile[ir, im]
            )

            original_charge += dq
            original_abs_charge += abs(dq)

            j0 = int(math.floor((z - zs[0]) / h))
            i0 = int(math.floor((rho - rhos[0]) / h))

            if not (
                0 <= j0 < len(zs) - 1
                and 0 <= i0 < len(rhos) - 1
            ):
                raise ValueError(
                    "Source lies outside computational domain"
                )

            tz = (z - zs[j0]) / h
            tr = (rho - rhos[i0]) / h

            corners = []

            for dj, wz in ((0, 1-tz), (1, tz)):
                for di, wri in ((0, 1-tr), (1, tr)):
                    j, i = j0 + dj, i0 + di

                    if (
                        1 <= j < len(zs) - 1
                        and 0 <= i < len(rhos) - 1
                        and math.hypot(
                            zs[j], rhos[i]
                        ) <= source_radius_m + 1e-12
                    ):
                        corners.append(
                            (j, i, max(0.0, wz*wri))
                        )

            if not corners:
                raise ValueError(
                    "No onboard node near B7 source"
                )

            norm = sum(w for _, _, w in corners)

            if norm <= 0:
                raise ValueError(
                    "Degenerate B7 transfer stencil"
                )

            if len(corners) < 4:
                truncated += 1

            for j, i, weight in corners:
                qnodes[j-1, i] += dq * weight / norm

                max_spread = max(
                    max_spread,
                    math.hypot(
                        zs[j] - z,
                        rhos[i] - rho,
                    ),
                )

    axis_weights = rhos[:-1].copy()
    axis_weights[0] = h / 8

    volume = (
        2 * math.pi * h*h
        * axis_weights[None, :]
    )

    jphi = qnodes / volume

    if not np.isfinite(jphi).all():
        raise ArithmeticError(
            "Nonfinite B7 discrete current"
        )

    zz = zs[1:-1, None]
    rr = rhos[None, :-1]
    rad = np.hypot(zz, rr)

    costheta = np.divide(
        zz,
        rad,
        out=np.zeros_like(rad),
        where=rad > 0,
    )

    moment_rows = []

    for ell, amplitude in enumerate(amps, start=1):
        analytic = (
            -4 * math.pi / math.sqrt(2)
            * float(amplitude)
            * source_radius_m**(ell+1)
        )

        obtained = float(
            np.sum(
                qnodes * rad**ell
                * eval_legendre(ell, costheta)
            )
        )

        ratio = (
            obtained / analytic
            if analytic else None
        )

        moment_rows.append({
            "ell": ell,
            "analytic_volume_multipole": analytic,
            "deposited_volume_multipole": obtained,
            "moment_ratio": ratio,
            "relative_moment_error":
                abs(ratio - 1) if ratio is not None else None,
        })

    support = (
        rad <= source_radius_m + 1e-12
    )

    neutrality = (
        abs(float(qnodes.sum()))
        / max(float(np.sum(abs(qnodes))), 1e-300)
    )

    input_neutrality = (
        abs(original_charge)
        / max(original_abs_charge, 1e-300)
    )

    return {
        "j_phi": jphi.reshape(-1),
        "cell_charge": qnodes,
        "net_charge_relative_residual": neutrality,
        "input_quadrature_neutrality": input_neutrality,
        "source_outside_support_count":
            int(np.count_nonzero(qnodes[~support])),
        "radial_order": radial_order,
        "angular_order": angular_order,
        "max_transfer_stencil_spread_m": max_spread,
        "truncated_stencil_sample_count": truncated,
        "moment_rows": moment_rows,
        "higher_multipole_fidelity_certified": False,
        "local_source_density_convergence_certified": False,
        "loaded_earth_reaction_certified": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }


def r3b_aligned_source_audit(h=0.25):
    """Project original R3B multipoles; solve only unloaded Poisson.

    The B7 charge distribution is used rather than the earlier M4B1
    surrogate electric dipole. Results depend on finite-box Dirichlet
    boundaries as well as on source discretization.

    No Earth-loaded force is computed by this preflight.
    """

    from scipy.sparse.linalg import spsolve

    from .hook17_fdual_f_global_mirror_prefight import (
        fit_exterior_multipoles,
        PRIMARY_FIT_RADIUS_M,
        PRIMARY_LMAX,
    )

    from .hook17_fdual_f_loaded_payload_homotopy import (
        _construct_global_mirror_phi,
        _fields_from_potentials,
    )

    from .hook17_r3b_m4b1_source_recovery import (
        assemble_original_aligned_source,
    )

    source = assemble_original_aligned_source(float(h))
    field = source["field"]

    fit = fit_exterior_multipoles(
        field,
        PRIMARY_FIT_RADIUS_M,
        PRIMARY_LMAX,
    )

    raw_phi = _construct_global_mirror_phi(
        field, fit
    )

    target_phi = source["target_phi"]

    multiplier = float(
        np.sum(raw_phi * target_phi)
        / np.sum(raw_phi * raw_phi)
    )

    normalization_error = float(
        np.linalg.norm(
            raw_phi * multiplier - target_phi
        ) / np.linalg.norm(target_phi)
    )

    if normalization_error > 1e-10:
        raise ArithmeticError(
            "R3B normalization provenance failure"
        )

    amps = (
        np.asarray(
            fit["boundary_amplitudes"],
            dtype=float,
        ) * multiplier
    )

    deposited = deposit_b7_to_axisymmetric_nodes(
        field["zs"],
        field["rhos"],
        field["h"],
        amps,
    )

    recovered = spsolve(
        source["operators"]["k_phi"],
        deposited["j_phi"],
    )

    phi = np.zeros_like(field["rho_grid"])

    phi[1:-1, :-1] = recovered.reshape(
        phi[1:-1, :-1].shape
    )

    zero = np.zeros_like(phi)

    e_rec = _fields_from_potentials(
        phi,
        zero,
        field["rho_grid"],
        field["h"],
    )

    e_target = _fields_from_potentials(
        target_phi,
        zero,
        field["rho_grid"],
        field["h"],
    )

    radius = np.hypot(
        field["z_grid"],
        field["rho_grid"],
    )

    mask = (
        (radius > 2.4)
        & (radius < 4.0)
    )

    er = np.stack((
        e_rec["e_rho"][mask],
        e_rec["e_z"][mask],
    ))

    et = np.stack((
        e_target["e_rho"][mask],
        e_target["e_z"][mask],
    ))

    exterior_error = float(
        np.linalg.norm(er - et)
        / np.linalg.norm(et)
    )

    return {
        "branch": BRANCH,
        "h_m": float(h),
        "original_r3b_unloaded_field_energy_j":
            1.5429162116460216,
        "original_b7_unloaded_field_energy_j":
            1.5473042949759672,
        "normalization_provenance_relative_error":
            normalization_error,
        "source": {
            key: value
            for key, value in deposited.items()
            if key not in ("j_phi", "cell_charge")
        },
        "unloaded_electric_exterior_relative_l2_error":
            exterior_error,
        "source_is_analytic_b7_radial_profile": True,
        "deposition_reconstructs_exact_B7_continuum_source":
            False,
        "loaded_earth_solver_executed": False,
        "outer_boundary_artifact_excluded": False,
        "grid_convergence_certified": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
    }
