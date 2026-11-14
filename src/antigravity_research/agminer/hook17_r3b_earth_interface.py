"""B17-M1: local, planar, two-U(1) material-interface preflight.

Scientific question
-------------------
Can the original R3B mixed-carrier field match across vacuum, air,
and dense ground interfaces without imposing undocumented surface sources?

This is a necessary-condition test, not a complete Earth-loaded BVP.

Same-action constitutive backbone (R3X1)
----------------------------------------
L = 0.5*(E_X^2 + E_Y^2 - B_X^2 - B_Y^2)
    + theta*(E_X.B_Y + E_Y.B_X)

D_X = E_X + theta*B_Y
D_Y = E_Y + theta*B_X
H_X = B_X - theta*E_Y
H_Y = B_Y - theta*E_X

Theta is the frozen-density portal coefficient already used in the
corrected Lorentzian R3X1/R3C1 reduced solver.

Without free interface sources, exact static Maxwell conditions require
continuity of tangential E, normal B, normal D, and tangential H.

Limitations
-----------
- Flat local interface; no globally sourced 3D Earth/craft solution.
- Frozen material-density law, not dynamical matter equations.
- Field-only Hamiltonian density, not complete operational energy.
- No microscopic apparatus, hull reaction, atmosphere flow or gravity solve.
- The lift classifier is arithmetic only; force must be independently derived.

Claim class:
EXACT_LOCAL_PLANAR_FROZEN_THETA_JUMP_NECESSITY_ONLY.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .hook17_concurrent_u1_fieldstrength_metric import (
    REFERENCE_PORTAL_SCALE_EV,
)
from .hook17_f2_strong_payload_loading_rescue import (
    loading_coefficient_z,
)


def theta_for_density(
    density_kg_m3: float,
    portal_scale_ev: float = REFERENCE_PORTAL_SCALE_EV,
) -> float:
    """Return theta = -(Z-1) for the frozen 1-keV portal law."""
    if not math.isfinite(density_kg_m3) or density_kg_m3 < 0:
        raise ValueError("Density must be finite and nonnegative")
    if not math.isfinite(portal_scale_ev) or portal_scale_ev <= 0:
        raise ValueError("Portal scale must be positive and finite")

    z = loading_coefficient_z(
        np.array([density_kg_m3]), portal_scale_ev
    )
    return float(1.0 - z[0])


def _vector(value):
    array = np.asarray(value, dtype=float)
    if array.shape != (3,) or not np.isfinite(array).all():
        raise ValueError("Expected a finite three-vector")
    return array.copy()


def _normal(value):
    vector = _vector(value)
    magnitude = float(np.linalg.norm(vector))
    if magnitude < 1e-12:
        raise ValueError("Interface normal must be nonzero")
    return vector / magnitude


@dataclass(frozen=True)
class TwoCarrierState:
    """Canonical three-vector fields in both protected U(1) sectors."""

    e_x: np.ndarray
    b_x: np.ndarray
    e_y: np.ndarray
    b_y: np.ndarray

    def __post_init__(self):
        for name in ("e_x", "b_x", "e_y", "b_y"):
            object.__setattr__(
                self, name, _vector(getattr(self, name))
            )


def constitutive_fields(state: TwoCarrierState, theta: float):
    """Return D_X, D_Y, H_X, H_Y with corrected Lorentzian signs."""
    return (
        state.e_x + theta * state.b_y,
        state.e_y + theta * state.b_x,
        state.b_x - theta * state.e_y,
        state.b_y - theta * state.e_x,
    )


def field_only_energy_density(state: TwoCarrierState) -> float:
    """Positive free-carrier Hamiltonian density, in canonical units."""
    return 0.5 * sum(
        float(vector @ vector)
        for vector in (state.e_x, state.b_x, state.e_y, state.b_y)
    )


def _parts(vector, normal):
    perpendicular = float(vector @ normal) * normal
    return perpendicular, vector - perpendicular


def match_no_free_interface(
    state: TwoCarrierState,
    theta_before: float,
    theta_after: float,
    normal=(0.0, 0.0, 1.0),
) -> TwoCarrierState:
    """Solve the static Maxwell interface conditions without free sheets.

    Delta theta = theta_after - theta_before.

    E_X,n(after) = E_X,n(before) - Delta theta * B_Y,n
    E_Y,n(after) = E_Y,n(before) - Delta theta * B_X,n

    B_X,t(after) = B_X,t(before) + Delta theta * E_Y,t
    B_Y,t(after) = B_Y,t(before) + Delta theta * E_X,t

    E_t and B_n are continuous. This is exact algebra for the
    declared *piecewise-constant* theta model.
    """
    n = _normal(normal)

    if not (
        math.isfinite(theta_before)
        and math.isfinite(theta_after)
    ):
        raise ValueError("Nonfinite theta")

    delta = theta_after - theta_before

    ex_n, ex_t = _parts(state.e_x, n)
    ey_n, ey_t = _parts(state.e_y, n)
    bx_n, bx_t = _parts(state.b_x, n)
    by_n, by_t = _parts(state.b_y, n)

    return TwoCarrierState(
        e_x=ex_t + ex_n - delta * by_n,
        e_y=ey_t + ey_n - delta * bx_n,
        b_x=bx_n + bx_t + delta * ey_t,
        b_y=by_n + by_t + delta * ex_t,
    )


def jump_residuals(
    before: TwoCarrierState,
    after: TwoCarrierState,
    theta_before: float,
    theta_after: float,
    normal=(0.0, 0.0, 1.0),
):
    """Measure all eight boundary-condition residual groups."""
    n = _normal(normal)

    dx0, dy0, hx0, hy0 = constitutive_fields(
        before, theta_before
    )
    dx1, dy1, hx1, hy1 = constitutive_fields(
        after, theta_after
    )

    def normal_residual(a, b):
        return abs(float((b - a) @ n))

    def tangential_residual(a, b):
        difference = b - a
        return float(np.linalg.norm(
            difference - float(difference @ n) * n
        ))

    return {
        "e_x_t": tangential_residual(before.e_x, after.e_x),
        "e_y_t": tangential_residual(before.e_y, after.e_y),
        "b_x_n": normal_residual(before.b_x, after.b_x),
        "b_y_n": normal_residual(before.b_y, after.b_y),
        "d_x_n": normal_residual(dx0, dx1),
        "d_y_n": normal_residual(dy0, dy1),
        "h_x_t": tangential_residual(hx0, hx1),
        "h_y_t": tangential_residual(hy0, hy1),
    }


def source_sheet_needed_to_preserve_fields(
    state: TwoCarrierState,
    theta_before: float,
    theta_after: float,
    normal=(0.0, 0.0, 1.0),
):
    """Required canonical free sheets if unchanged fields are imposed.

    These are mathematical surface-source amplitudes, NOT SI charge or
    current densities and NOT a validated microscopic source.
    """
    n = _normal(normal)
    delta = theta_after - theta_before

    return {
        "electric_x_sheet_canonical":
            float(delta * (state.b_y @ n)),
        "electric_y_sheet_canonical":
            float(delta * (state.b_x @ n)),
        "current_x_tangent_canonical":
            (-delta * np.cross(n, state.e_y)).tolist(),
        "current_y_tangent_canonical":
            (-delta * np.cross(n, state.e_x)).tolist(),
    }


def original_mirror_state(br: float, bz: float) -> TwoCarrierState:
    """R3B fitted exterior E_X=B_Y, with other sectors initially zero."""
    vector = np.array([br, 0.0, bz])
    zero = np.zeros(3)

    return TwoCarrierState(
        e_x=vector,
        b_x=zero,
        e_y=zero,
        b_y=vector,
    )


def classify_lift(
    craft_mass_kg: float,
    derived_whole_craft_field_force_n: float | None,
    g_m_s2: float = 9.80665,
):
    """Screen the two success milestones without inventing field force.

    An actual certificate additionally requires a physical force from
    the full action, convergence, source-off subtraction, whole-craft
    reaction, Earth/environment ledger, and stability.
    """
    if (
        not math.isfinite(craft_mass_kg)
        or craft_mass_kg <= 0
        or not math.isfinite(g_m_s2)
        or g_m_s2 <= 0
    ):
        raise ValueError("Positive finite mass and gravity required")

    weight = craft_mass_kg * g_m_s2

    if derived_whole_craft_field_force_n is None:
        return {
            "gravity_n": weight,
            "field_force_n": None,
            "net_upward_force_n": None,
            "gravity_cancellation": None,
            "pure_field_lift": None,
            "auxiliary_hover_thrust_n": None,
            "status": "NOT_DETERMINED",
        }

    force = float(derived_whole_craft_field_force_n)

    if not math.isfinite(force):
        raise ValueError("Nonfinite whole-craft force")

    return {
        "gravity_n": weight,
        "field_force_n": force,
        "net_upward_force_n": force - weight,
        "gravity_cancellation": force >= weight,
        "pure_field_lift": force > weight,
        "auxiliary_hover_thrust_n": max(0.0, weight - force),
        "status": "ARITHMETIC_ONLY_REQUIRES_FORCE_CERTIFICATE",
    }
