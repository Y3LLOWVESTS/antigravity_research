"""B17-M4B0: finite-box, source-fixed, two-carrier Earth-loading control.

This run reuses the R3X1 corrected Lorentzian static equations:

    [ K_phi       lambda*C ] [phi] = [j_phi]
    [ -lambda*D   K_a      ] [A]   [j_A]

The off-diagonal matrices obey weighted variational reciprocity:
    W_a D = C.T W_phi.

A new net-neutral electric dipole and an azimuthal magnetic current
are compactly supported inside the onboard 2m source region. Their
unloaded Earth-facing axial field is normalized against R3B.

IMPORTANT: These are new phenomenological source controls, NOT an
exact physical realization of the original R3B 1.542916-J field.

Finite ground and atmospheric material respond through frozen-density
theta. The complete coupled carrier BVP is solved directly, rather
than holding the exterior field fixed.

The result does NOT establish microscopic sources, whole-craft force,
full Earth gravity, hull stresses, source work, continuum convergence,
or complete operating energy.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.sparse import bmat, diags
from scipy.sparse.linalg import spsolve

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    SOURCE_RADIUS_M,
)
from .hook17_fdual_f_loaded_payload_homotopy import (
    _a12c_potential_field,
    _build_elliptic_operators,
    _build_same_action_coupling,
    _fields_from_potentials,
)
from .hook17_f2_strong_payload_loading_rescue import (
    loading_coefficient_z,
)
from .hook17_r3b_exterior_transmission import (
    fitted_b_field,
    normalized_r3b_fit,
)


@dataclass(frozen=True)
class MaterialGeometry:
    ground_top_relative_z_m: float = -3.0
    ground_radius_m: float = 2.0
    ground_depth_m: float = 1.0
    ground_density_kg_m3: float = 2000.0
    air_density_kg_m3: float = 1.2
    enclosure_radius_m: float = 2.25
    interface_width_m: float = 0.25

    def __post_init__(self):
        if self.ground_top_relative_z_m >= -(SOURCE_RADIUS_M + 0.2):
            raise ValueError("Ground overlaps onboard source")

        for key in (
            "ground_radius_m",
            "ground_depth_m",
            "ground_density_kg_m3",
            "enclosure_radius_m",
            "interface_width_m",
        ):
            value = getattr(self, key)
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"Invalid {key}")

        if (
            not math.isfinite(self.air_density_kg_m3)
            or self.air_density_kg_m3 < 0
        ):
            raise ValueError("Invalid atmospheric density")

        if self.enclosure_radius_m < SOURCE_RADIUS_M + 0.1:
            raise ValueError("Enclosure does not contain onboard source")


def _smooth_below(x, edge, width):
    """Compact C1 transition; exactly zero outside its finite support."""
    u = np.clip((x - edge + width) / (2 * width), 0.0, 1.0)
    return 1.0 - (3 * u * u - 2 * u * u * u)


def material_density(
    field,
    geometry,
    include_air=True,
    include_earth=True,
):
    r = field["rho_grid"]
    z = field["z_grid"]

    radial_ball = np.hypot(r, z)

    outside_enclosure = 1.0 - _smooth_below(
        radial_ball,
        geometry.enclosure_radius_m,
        geometry.interface_width_m,
    )

    air = (
        geometry.air_density_kg_m3 * outside_enclosure
        if include_air
        else np.zeros_like(r)
    )

    disk = _smooth_below(
        r,
        geometry.ground_radius_m,
        geometry.interface_width_m,
    )

    below_top = _smooth_below(
        z,
        geometry.ground_top_relative_z_m,
        geometry.interface_width_m,
    )

    above_bottom = 1.0 - _smooth_below(
        z,
        geometry.ground_top_relative_z_m - geometry.ground_depth_m,
        geometry.interface_width_m,
    )

    earth_fraction = disk * below_top * above_bottom

    ground = (
        geometry.ground_density_kg_m3 * earth_fraction
        if include_earth
        else np.zeros_like(r)
    )

    # Replace air where ground occupies space.
    density = air * (1.0 - earth_fraction) + ground

    return density, earth_fraction


def _assemble_baseline(h, reference):
    """Construct new finite-support source controls, not exact R3B."""
    field = _a12c_potential_field(float(h))
    rho = field["rho_grid"]
    z = field["z_grid"]

    ops = _build_elliptic_operators(
        field["rhos"],
        field["zs"],
        float(h),
    )

    inside = np.hypot(rho, z) <= SOURCE_RADIUS_M
    e_mask = inside[1:-1, :-1].reshape(-1)
    b_mask = inside[1:-1, 1:-1].reshape(-1)

    a_template = field["a_phi"] / math.sqrt(2.0)

    j_a = (
        ops["k_a"]
        @ a_template[1:-1, 1:-1].reshape(-1)
    ) * b_mask

    r_e = rho[1:-1, :-1].reshape(-1)
    z_e = z[1:-1, :-1].reshape(-1)

    envelope = (
        np.exp(-np.square(np.hypot(r_e, z_e) / 0.82))
        * e_mask
    )

    axis_weight = np.where(r_e == 0.0, h / 8.0, r_e)

    center = (
        np.dot(axis_weight * envelope, z_e)
        / np.sum(axis_weight * envelope)
    )

    j_phi_shape = (z_e - center) * envelope

    neutrality = abs(
        float(np.dot(axis_weight, j_phi_shape))
    ) / max(
        float(np.dot(axis_weight, np.abs(j_phi_shape))),
        1e-99,
    )

    a0 = spsolve(ops["k_a"], j_a)

    a_full = np.zeros_like(rho)
    a_full[1:-1, 1:-1] = a0.reshape(
        a_full[1:-1, 1:-1].shape
    )

    zero = np.zeros_like(rho)

    b_map = _fields_from_potentials(
        zero,
        a_full,
        rho,
        h,
    )

    axis_index = int(np.argmin(np.abs(field["zs"] + 3.0)))

    b_here = float(b_map["b_z"][axis_index, 0])

    b_reference = fitted_b_field(
        reference["coefficients"],
        0.0,
        -3.0,
    )[1] * math.sqrt(reference["amplitude_squared_scale"])

    if abs(b_here) < 1e-8:
        raise RuntimeError("Magnetic source produces no axial field")

    magnetic_scale = b_reference / b_here

    j_a *= magnetic_scale
    a0 *= magnetic_scale

    phi_unit = spsolve(
        ops["k_phi"],
        j_phi_shape,
    )

    phi_full = np.zeros_like(rho)

    phi_full[1:-1, :-1] = phi_unit.reshape(
        phi_full[1:-1, :-1].shape
    )

    e_unit = float(
        _fields_from_potentials(
            phi_full,
            zero,
            rho,
            h,
        )["e_z"][axis_index, 0]
    )

    if abs(e_unit) < 1e-12:
        raise RuntimeError("Electric dipole produces no axial field")

    electric_scale = -b_reference / e_unit

    return {
        "field": field,
        "operators": ops,
        "j_phi": j_phi_shape * electric_scale,
        "j_a": j_a,
        "phi0": phi_unit * electric_scale,
        "a0": a0,
        "charge_neutrality_relative": neutrality,
        "source_mask_phi": e_mask,
        "source_mask_a": b_mask,
        "source_npoints_phi": int(np.count_nonzero(j_phi_shape)),
        "source_npoints_a": int(np.count_nonzero(j_a)),
        "reference_axis_b": float(b_reference),
    }


def _solve_fixed_sources(base, beta, fraction=1.0):
    """Direct sparse solve of the corrected Lorentzian carrier equations."""
    if not math.isfinite(fraction) or not 0 <= fraction <= 1:
        raise ValueError("Loading fraction must lie in [0,1]")

    ops = base["operators"]
    field = base["field"]

    coupling = _build_same_action_coupling(
        field["rhos"],
        field["zs"],
        field["h"],
        beta,
        ops,
    )

    matrix = bmat(
        [
            [ops["k_phi"], fraction * coupling["c"]],
            [-fraction * coupling["d"], ops["k_a"]],
        ],
        format="csr",
    )

    rhs = np.r_[base["j_phi"], base["j_a"]]

    solution = spsolve(matrix, rhs)

    if not np.isfinite(solution).all():
        raise ArithmeticError("Nonfinite coupled carrier solution")

    residual = float(
        np.linalg.norm(matrix @ solution - rhs)
        / max(np.linalg.norm(rhs), 1.0)
    )

    n_phi = ops["k_phi"].shape[0]

    phi = np.zeros_like(field["rho_grid"])
    a = np.zeros_like(phi)

    phi[1:-1, :-1] = solution[:n_phi].reshape(
        phi[1:-1, :-1].shape
    )

    a[1:-1, 1:-1] = solution[n_phi:].reshape(
        a[1:-1, 1:-1].shape
    )

    em = _fields_from_potentials(
        phi,
        a,
        field["rho_grid"],
        field["h"],
    )

    dot_eb = (
        em["e_rho"] * em["b_rho"]
        + em["e_z"] * em["b_z"]
    )

    # Exact weighted reciprocity audit with corrected scalar axis weight.
    nz = ops["nz_inner"]

    w_r = np.asarray(field["rhos"][:-1], dtype=float).copy()
    w_r[0] = field["h"] / 8.0

    w_phi = diags(np.tile(w_r, nz), format="csr")
    w_a = diags(
        np.tile(field["rhos"][1:-1], nz),
        format="csr",
    )

    lhs = w_a @ coupling["d"]
    rhs_cross = coupling["c"].T @ w_phi

    difference = (lhs - rhs_cross).tocsr()

    scale = max(
        float(np.max(np.abs(lhs.data))) if lhs.nnz else 0.0,
        1.0,
    )

    reciprocity = (
        float(np.max(np.abs(difference.data))) / scale
        if difference.nnz
        else 0.0
    )

    carrier_energy = 0.5 * float(
        np.sum(
            2 * math.pi
            * field["rho_grid"]
            * field["h"]**2
            * (
                em["e_rho"]**2
                + em["e_z"]**2
                + em["b_rho"]**2
                + em["b_z"]**2
            )
        )
    ) * EV_J / HBAR_C_EV_M

    return {
        "phi": phi,
        "a": a,
        "em": em,
        "dot": dot_eb,
        "residual": residual,
        "coupling": coupling,
        "relative_weighted_reciprocity": reciprocity,
        "carrier_energy_j": carrier_energy,
    }


def run_case(
    h=0.25,
    portal_scale_ev=1000.0,
    geometry=None,
    include_air=False,
    fractions=(0.0, 1.0),
):
    """Compare unloaded and loaded fields with identical onboard sources."""
    if geometry is None:
        geometry = MaterialGeometry()

    if not 0.1 <= h <= 0.4:
        raise ValueError("M4B0 grid must lie between 0.1 and 0.4")

    if not math.isfinite(portal_scale_ev) or portal_scale_ev <= 0:
        raise ValueError("Invalid portal scale")

    reference = normalized_r3b_fit(0.05)
    base = _assemble_baseline(h, reference)

    density, earth_fraction = material_density(
        base["field"],
        geometry,
        include_air,
        True,
    )

    beta = 1.0 - loading_coefficient_z(
        density,
        portal_scale_ev,
    )

    # Matched UNLOADED sigma comparator, not a physical source certificate.
    amplitude_factor = (portal_scale_ev / 1000.0)**2

    base["j_phi"] *= amplitude_factor
    base["j_a"] *= amplitude_factor

    field = base["field"]
    volume = (
        2 * math.pi
        * field["rho_grid"]
        * field["h"]**2
    )

    ground_density = geometry.ground_density_kg_m3 * earth_fraction

    air_density = (
        density - ground_density
        if include_air
        else np.zeros_like(density)
    )

    states = {}

    for fraction in fractions:
        state = _solve_fixed_sources(base, beta, fraction)

        sigma = (
            -2.0
            * HBAR_C_EV_M**2
            * state["dot"]
            / portal_scale_ev**4
        )

        acceleration = (
            -C_LIGHT_M_S**2
            * np.gradient(
                sigma,
                field["h"],
                axis=0,
                edge_order=2,
            )
        )

        ground_tracer = float(
            np.sum(volume * ground_density * acceleration)
        )

        air_tracer = float(
            np.sum(volume * air_density * acceleration)
        )

        mask = (
            (earth_fraction > 0.3)
            & (field["rho_grid"] < geometry.ground_radius_m)
        )

        states[str(fraction)] = {
            "loaded_solve_residual": state["residual"],
            "carrier_energy_j": state["carrier_energy_j"],
            "ground_frozen_tracer_force_n": ground_tracer,
            "atmosphere_frozen_tracer_force_n": air_tracer,
            "earth_tracer_accel_min_m_s2":
                float(np.min(acceleration[mask])),
            "earth_tracer_accel_max_m_s2":
                float(np.max(acceleration[mask])),
            "sigma_max_in_earth":
                float(np.max(np.abs(sigma[mask]))),
            "same_action_weighted_relative_residual":
                state["relative_weighted_reciprocity"],
        }

    return {
        "branch": "032H17A12D1R3X3B17-M4B0",
        "classification":
            "FINITE_BOX_STATIC_SOURCE_FIXED_TWO_U1_LOADING_CONTROL",
        "h_m": h,
        "portal_scale_ev": portal_scale_ev,
        "air_included": include_air,
        "reference_r3b_preloaded_j":
            reference["preloaded_energy_j"],
        "constructed_source_is_original_r3b": False,
        "reconstructed_source_current_supported_within_2m": True,
        "electric_relative_net_charge":
            base["charge_neutrality_relative"],
        "source_electric_npoints":
            base["source_npoints_phi"],
        "source_magnetic_npoints":
            base["source_npoints_a"],
        "states": states,
        "full_earth_halfspace": False,
        "hull_material_solved": False,
        "microscopic_source_realized": False,
        "grid_convergence_certified": False,
        "interface_profile_convergence_certified": False,
        "finite_box_artifact_excluded": False,
        "complete_energy_j": None,
        "whole_craft_force_n": None,
        "gravity_cancellation": None,
        "pure_antigravity_lift": None,
        "006d_replaced": False,
    }
