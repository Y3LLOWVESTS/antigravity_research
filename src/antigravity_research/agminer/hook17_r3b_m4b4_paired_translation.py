"""B17-M4B4: paired Earth/craft translations of a reduced carrier action.

PURPOSE
-------
The previous M4B2 calculation varied the finite Earth target while
holding the onboard source fixed. This independent gate varies BOTH
Earth and the onboard source, with its vacuum enclosure translated
together with the source.

For a translation-invariant interaction action:

    dS_int/dz_E + dS_int/dz_C = 0

This identity is a prerequisite for interpreting reduced-action
interaction gradients as a legitimate reciprocal coupling.

The reference Earth-free configuration is subtracted at each source
position to isolate the extra finite-ground interaction.

THEORY
------
Uses the R3X1 corrected Lorentzian two-carrier static system:

    [ K_phi       C ] [phi] = [j_phi]
    [ -D        K_a ] [ A ] = [j_A]

where weighted reciprocity requires Wa D = C.T Wphi.

The weighted stationary action has the source-reduced value:

    S_on = N/2 * (-phi.T Wphi j_phi + A.T Wa j_A)

with N = 2*pi*h^2*eV_J/(hbar*c)_eVm.

The envelope theorem yields:

    dS_on = N [
       phi.T Wphi (dC A - dj_phi)
       + A.T Wa dj_A
    ]

at fixed stationary fields. This derivative is evaluated independently
from centered differences of fully re-solved on-shell actions.

IMPORTANT LIMITATIONS
---------------------
- M4B1 APPROXIMATE R3B-aligned source, not exact R3B or original B7.
- A virtual source shift is nodal interpolation, NOT a physically
  continuous moving-source current and Ward/continuity solution.
- The ground target and enclosure are finite; fixed outer Dirichlet
  boundaries can supply unmodeled numerical forces.
- Material density is prescribed and static, not mechanically varied.
- Physical gravity, matter stress, hull, atmospheric momentum,
  microscopic source, and the full spacetime metric are incomplete.
- Action derivatives have force dimensions, but their physical-force
  signs and identification are NOT certified here.
- No whole-craft propulsion, antigravity or <10MJ device claim.
"""

from __future__ import annotations

import math
import numpy as np

from .hook17_f2_strong_payload_loading_rescue import (
    loading_coefficient_z,
)
from .hook17_fdual_f_loaded_payload_homotopy import (
    _build_same_action_coupling,
)
from .hook17_r3b_m4b_sparse_earth_loading import (
    MaterialGeometry,
    _smooth_below,
    _solve_fixed_sources,
)
from .hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)
from .hook17_r3b_m4b2_earth_variational_audit import (
    _weights,
    _on_shell_action,
)

BRANCH = "032H17A12D1R3X3B17-M4B4"


def translate_current_z(current, source, shift_m, magnetic):
    """Subgrid nodal shift used ONLY for a virtual-source audit.

    Linear interpolation conserves the basic array structure, but
    introduces a one-cell support skirt and discrete derivative error.
    It is not a dynamical current-continuity construction.
    """
    field = source["field"]

    nz = len(field["zs"]) - 2
    nr = len(field["rhos"]) - (2 if magnetic else 1)

    z = np.asarray(field["zs"][1:-1])
    values = np.asarray(current).reshape(nz, nr)
    shifted = np.empty_like(values)

    for j in range(nr):
        shifted[:, j] = np.interp(
            z - shift_m,
            z,
            values[:, j],
            left=0.0,
            right=0.0,
        )

    return shifted.reshape(-1)


def shifted_source(source, scale_ev, craft_shift_m):
    """Translate the two fixed current controls together."""
    amplifier = (scale_ev / 1000.0)**2

    jp = translate_current_z(
        source["j_phi"],
        source,
        craft_shift_m,
        False,
    )
    ja = translate_current_z(
        source["j_a"],
        source,
        craft_shift_m,
        True,
    )

    return {
        **source,
        "j_phi": amplifier * jp,
        "j_a": amplifier * ja,
    }


def shifted_material(
    source,
    earth_z_m,
    craft_z_m,
    scale_ev,
    *,
    earth_present,
):
    """Finite Earth, atmosphere, and moving vacuum enclosure.

    Air is prescribed outside the craft-centered vacuum enclosure.
    Where the finite Earth target occupies space, it displaces air.

    Moving the craft also moves its vacuum enclosure.
    The background matter itself is not dynamically evolved.
    """
    geometry = MaterialGeometry()
    field = source["field"]

    r = field["rho_grid"]
    z = field["z_grid"]
    width = geometry.interface_width_m

    outside_enclosure = 1.0 - _smooth_below(
        np.hypot(r, z - craft_z_m),
        geometry.enclosure_radius_m,
        width,
    )

    disk = _smooth_below(
        r,
        geometry.ground_radius_m,
        width,
    )

    below_top = _smooth_below(
        z,
        earth_z_m + geometry.ground_top_relative_z_m,
        width,
    )

    above_bottom = 1.0 - _smooth_below(
        z,
        (
            earth_z_m
            + geometry.ground_top_relative_z_m
            - geometry.ground_depth_m
        ),
        width,
    )

    if earth_present:
        ground_fraction = disk * below_top * above_bottom
    else:
        ground_fraction = np.zeros_like(z)

    density = (
        geometry.air_density_kg_m3
        * outside_enclosure
        * (1.0 - ground_fraction)
        + geometry.ground_density_kg_m3 * ground_fraction
    )

    beta = 1.0 - loading_coefficient_z(
        density,
        scale_ev,
    )

    return beta, density, ground_fraction


def cross_c(source, beta):
    """Retrieve the variational cross-carrier operator."""
    field = source["field"]

    return _build_same_action_coupling(
        field["rhos"],
        field["zs"],
        field["h"],
        beta,
        source["operators"],
    )["c"]


def solve_action(
    source,
    scale_ev,
    earth_z_m,
    craft_z_m,
    earth_present,
):
    """Re-solve both carriers with identical physical source scale."""
    currents = shifted_source(
        source,
        scale_ev,
        craft_z_m,
    )

    beta, density, fraction = shifted_material(
        source,
        earth_z_m,
        craft_z_m,
        scale_ev,
        earth_present=earth_present,
    )

    state = _solve_fixed_sources(
        currents,
        beta,
        1.0,
    )

    action = _on_shell_action(
        state,
        currents,
        _weights(source),
    )

    return {
        "action_j": action,
        "state": state,
        "currents": currents,
        "beta": beta,
        "density": density,
        "ground_fraction": fraction,
    }


def pair_action(source, scale_ev, earth_z_m, craft_z_m):
    """Subtract the matching Earth-free atmospheric background."""
    loaded = solve_action(
        source, scale_ev,
        earth_z_m, craft_z_m,
        True,
    )

    air_only = solve_action(
        source, scale_ev,
        earth_z_m, craft_z_m,
        False,
    )

    return {
        "interaction_action_j":
            loaded["action_j"] - air_only["action_j"],
        "loaded": loaded,
        "air_only": air_only,
    }


def action_envelope_slope(
    source,
    center,
    plus,
    minus,
    delta,
):
    """Independent on-shell derivative from the envelope theorem.

    Both source-current derivatives and matter-coupling derivatives
    are included. No field-solution derivative is needed.
    """
    wp, wa, normalization = _weights(source)

    state = center["state"]
    phi = state["phi"][1:-1, :-1].reshape(-1)
    a = state["a"][1:-1, 1:-1].reshape(-1)

    cp = cross_c(source, plus["beta"])
    cm = cross_c(source, minus["beta"])

    d_c_a = (cp - cm) @ a / (2.0 * delta)

    d_jp = (
        plus["currents"]["j_phi"]
        - minus["currents"]["j_phi"]
    ) / (2.0 * delta)

    d_ja = (
        plus["currents"]["j_a"]
        - minus["currents"]["j_a"]
    ) / (2.0 * delta)

    return float(
        normalization
        * (
            np.dot(wp * phi, d_c_a - d_jp)
            + np.dot(wa * a, d_ja)
        )
    )


def source_support_check(source, shift_m):
    """Check support including the interpolation-induced skirt."""
    field = source["field"]

    moved = shifted_source(
        source,
        1000.0,
        shift_m,
    )

    z = np.asarray(field["zs"])[1:-1, None]
    phi_r = np.asarray(field["rhos"])[None, :-1]
    a_r = np.asarray(field["rhos"])[None, 1:-1]

    jp = moved["j_phi"].reshape(
        len(z),
        len(phi_r[0]),
    )
    ja = moved["j_a"].reshape(
        len(z),
        len(a_r[0]),
    )

    radius_phi = np.hypot(z, phi_r)
    radius_a = np.hypot(z, a_r)

    max_radius = max(
        (
            float(np.max(radius_phi[np.abs(jp) > 0]))
            if np.any(jp) else 0.0
        ),
        (
            float(np.max(radius_a[np.abs(ja) > 0]))
            if np.any(ja) else 0.0
        ),
    )

    enclosure_radius = MaterialGeometry().enclosure_radius_m

    return {
        "max_nodal_source_radius_m": max_radius,
        "inside_nominal_2m_region":
            max_radius <= 2.0 + 1e-12,
        "inside_enclosure_radius":
            max_radius <= enclosure_radius + 1e-12,
        "translated_source_is_exact_physical_current": False,
    }


def evaluate(
    h=0.25,
    scale_ev=21147.0,
    step_m=2e-4,
):
    """Evaluate the paired translation derivatives and controls."""
    if not (
        math.isfinite(h)
        and 0.15 <= h <= 0.30
    ):
        raise ValueError("Grid outside established M4B1 range")

    if not (
        math.isfinite(scale_ev)
        and scale_ev > 0
    ):
        raise ValueError("Invalid portal scale")

    if not (
        math.isfinite(step_m)
        and 1e-7 <= step_m < 0.01
    ):
        raise ValueError("Invalid translation step")

    source = assemble_original_aligned_source(float(h))

    center = pair_action(source, scale_ev, 0.0, 0.0)

    earth_plus = pair_action(
        source, scale_ev, +step_m, 0.0
    )
    earth_minus = pair_action(
        source, scale_ev, -step_m, 0.0
    )

    craft_plus = pair_action(
        source, scale_ev, 0.0, +step_m
    )
    craft_minus = pair_action(
        source, scale_ev, 0.0, -step_m
    )

    earth_fd = (
        earth_plus["interaction_action_j"]
        - earth_minus["interaction_action_j"]
    ) / (2.0 * step_m)

    craft_fd = (
        craft_plus["interaction_action_j"]
        - craft_minus["interaction_action_j"]
    ) / (2.0 * step_m)

    def envelope(plus, minus):
        return (
            action_envelope_slope(
                source,
                center["loaded"],
                plus["loaded"],
                minus["loaded"],
                step_m,
            )
            - action_envelope_slope(
                source,
                center["air_only"],
                plus["air_only"],
                minus["air_only"],
                step_m,
            )
        )

    earth_env = envelope(
        earth_plus,
        earth_minus,
    )
    craft_env = envelope(
        craft_plus,
        craft_minus,
    )

    # Independently translate both systems simultaneously.
    both_plus = pair_action(
        source, scale_ev, +step_m, +step_m
    )
    both_minus = pair_action(
        source, scale_ev, -step_m, -step_m
    )

    common_fd = (
        both_plus["interaction_action_j"]
        - both_minus["interaction_action_j"]
    ) / (2.0 * step_m)

    defect = earth_env + craft_env

    normalized_defect = (
        abs(defect)
        / max(
            abs(earth_env),
            abs(craft_env),
            1e-20,
        )
    )

    return {
        "branch": BRANCH,
        "scope":
            "APPROX_R3B_SOURCE_FIXED_REDUCED_ACTION_EARTH_CRAFT_TRANSLATION_GATE",
        "h_m": float(h),
        "scale_ev": float(scale_ev),
        "translation_step_m": float(step_m),

        "earth_action_slope_j_m": earth_env,
        "craft_action_slope_j_m": craft_env,

        "earth_resolved_finite_difference_j_m": earth_fd,
        "craft_resolved_finite_difference_j_m": craft_fd,

        "earth_envelope_relative_error":
            abs(earth_fd - earth_env)
            / max(abs(earth_env), abs(earth_fd), 1e-20),

        "craft_envelope_relative_error":
            abs(craft_fd - craft_env)
            / max(abs(craft_env), abs(craft_fd), 1e-20),

        "paired_translation_defect_j_m": defect,
        "paired_translation_defect_fraction":
            normalized_defect,

        "common_shift_finite_difference_j_m":
            common_fd,

        "common_shift_minus_sum_j_m":
            common_fd - defect,

        "source_support_plus":
            source_support_check(source, +step_m),

        "source_support_minus":
            source_support_check(source, -step_m),

        "unloaded_r3b_field_capacity_reference_j":
            1.5429162116460216,

        "source_is_exact_b7_or_r3b": False,
        "source_translation_is_physically_sourced_motion":
            False,
        "convergence_certified": False,
        "finite_box_artifact_excluded": False,
        "same_action_full_noether_identity_certified":
            False,
        "source_current_transport_ward_identity_certified":
            False,
        "atmosphere_field_momentum_reaction_derived":
            False,
        "complete_craft_earth_matter_metric_action":
            False,
        "force_as_physical_thrust_certified": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
        "warning":
            "Action-gradient/translation audit only; "
            "not physical spacecraft lift",
    }
