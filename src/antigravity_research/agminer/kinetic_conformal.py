"""Shift-symmetric kinetic-conformal diagnostics for AGMINER 032V13.

PURPOSE
-------
Provide cheap analytical gates for physical metrics of the form

    g_phys = C(X) g

with exact scalar shift symmetry and a canonical kinetic sector.

SCIENTIFIC QUESTIONS
--------------------
1. Does a published kinetic-conformal matter coupling have the correct static
   external force sign for a localized spacelike scalar gradient?
2. Is the metric transformation invertible in the operating regime?
3. Can regular isolated matter source a nontrivial static shift-symmetric
   gradient when the conserved-current coefficient remains positive?
4. What is the bare exterior scalar-gradient energy if a legitimate source of
   shift charge is supplied by physics outside the minimal regular branch?

CLAIM LIMITS
------------
The exterior-energy functions are counterfactual lower-level diagnostics.
They omit source, support, control, activation, empirical, and backreaction
costs and must never be treated as complete operating-energy predictions.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


C_LIGHT = 299792458.0
EV_J = 1.602176634e-19
HBARC_EV_M = 1.973269804e-7
EV4_TO_J_M3 = EV_J / HBARC_EV_M**3


@dataclass(frozen=True)
class StaticShiftCurrentGate:
    """Inputs for the static conserved-current uniqueness gate."""

    current_coefficient_min: float
    regular_configuration: bool = True
    asymptotically_constant_field: bool = True
    explicit_shift_current_source: bool = False
    imposed_boundary_flux: bool = False
    topological_or_defect_sector: bool = False
    time_dependent_shift_background: bool = False

    @property
    def uniqueness_theorem_applies(self) -> bool:
        return (
            self.current_coefficient_min > 0.0
            and self.regular_configuration
            and self.asymptotically_constant_field
            and not self.explicit_shift_current_source
            and not self.imposed_boundary_flux
            and not self.topological_or_defect_sector
            and not self.time_dependent_shift_background
        )

    @property
    def nontrivial_localized_static_gradient_allowed(self) -> bool:
        return not self.uniqueness_theorem_applies


def required_ln_a_gradient_per_m(acceleration_m_s2: float) -> float:
    """Return |grad ln A| for g_phys=A^2 g in the weak static limit."""
    acceleration = float(acceleration_m_s2)
    if acceleration < 0.0:
        raise ValueError("acceleration_m_s2 must be nonnegative")
    return acceleration / C_LIGHT**2


def required_ln_c_gradient_per_m(acceleration_m_s2: float) -> float:
    """Return |grad ln C| for g_phys=C g in the weak static limit."""
    return 2.0 * required_ln_a_gradient_per_m(acceleration_m_s2)


def static_acceleration_m_s2(dlnc_dy: float, dy_dr_per_m: float) -> float:
    """Return radial acceleration for a declared positive kinetic variable Y."""
    return -0.5 * C_LIGHT**2 * float(dlnc_dy) * float(dy_dr_per_m)


def goldstone_linear_c(y: float) -> float:
    """Brax-Valageas A(chi)=1+chi with static chi=-Y, so C=(1-Y)^2."""
    value = float(y)
    if value < 0.0 or value >= 1.0:
        raise ValueError("goldstone linear static branch requires 0 <= Y < 1")
    return (1.0 - value) ** 2


def goldstone_linear_dlnc_dy(y: float) -> float:
    value = float(y)
    goldstone_linear_c(value)
    return -2.0 / (1.0 - value)


def goldstone_linear_jacobian_kinetic_eigenvalue(y: float) -> float:
    value = float(y)
    goldstone_linear_c(value)
    return 1.0 - value**2


def zgb_exponential_c(y: float) -> float:
    """Published C=exp(X/M^4) example evaluated on static X/M^4=-Y."""
    value = float(y)
    if value < 0.0:
        raise ValueError("Y must be nonnegative")
    return math.exp(-value)


def zgb_exponential_dlnc_dy(y: float) -> float:
    zgb_exponential_c(y)
    return -1.0


def zgb_exponential_jacobian_kinetic_eigenvalue(y: float) -> float:
    value = float(y)
    return zgb_exponential_c(value) * (1.0 + value)


def zgb_gaussian_c(y: float) -> float:
    """Published C=exp(-X^2/(2M^8)) example on static X/M^4=-Y."""
    value = float(y)
    if value < 0.0:
        raise ValueError("Y must be nonnegative")
    return math.exp(-0.5 * value**2)


def zgb_gaussian_dlnc_dy(y: float) -> float:
    value = float(y)
    zgb_gaussian_c(value)
    return -value


def zgb_gaussian_jacobian_kinetic_eigenvalue(y: float) -> float:
    value = float(y)
    return zgb_gaussian_c(value) * (1.0 + value**2)


def sign_flipped_linear_c(y: float) -> float:
    """Outward-sign target A=1-chi with static chi=-Y, hence C=(1+Y)^2.

    This is a diagnostic target for action matching. It is not assigned a
    microscopic UV completion by this module.
    """
    value = float(y)
    if value < 0.0 or value >= 1.0:
        raise ValueError("sign-flipped target uses the invertible domain 0 <= Y < 1")
    return (1.0 + value) ** 2


def sign_flipped_linear_dlnc_dy(y: float) -> float:
    value = float(y)
    sign_flipped_linear_c(value)
    return 2.0 / (1.0 + value)


def sign_flipped_linear_jacobian_kinetic_eigenvalue(y: float) -> float:
    value = float(y)
    sign_flipped_linear_c(value)
    return 1.0 - value**2


def static_shift_current_no_source(gate: StaticShiftCurrentGate) -> bool:
    """Return True when the positive-current uniqueness theorem forces grad phi=0.

    For a static equation of the form

        div[Z(x, grad phi) grad phi] = 0

    multiply by phi-phi_infinity and integrate over space. With vanishing
    boundary flux and Z>0, the boundary term vanishes and

        integral Z |grad phi|^2 dV = 0.

    Therefore every regular finite-energy isolated solution in this declared
    class has grad phi=0. Nontrivial configurations require an evasion listed
    in StaticShiftCurrentGate.
    """
    return gate.uniqueness_theorem_applies


def ev4_energy_density_j_m3(scale_ev: float) -> float:
    """Convert a natural-unit energy density scale M^4 to SI J/m^3."""
    scale = float(scale_ev)
    if scale <= 0.0:
        raise ValueError("scale_ev must be positive")
    return EV4_TO_J_M3 * scale**4


def sign_flipped_required_y_at_radius(
    acceleration_m_s2: float,
    radius_m: float,
) -> float:
    """Return Y for A=1+Y and a vacuum harmonic Y=K/r^4 profile.

    For C=(1+Y)^2 and Y=K/r^4,

        a = 4 c^2 Y / [r (1+Y)].
    """
    acceleration = float(acceleration_m_s2)
    radius = float(radius_m)
    if acceleration <= 0.0 or radius <= 0.0:
        raise ValueError("acceleration and radius must be positive")
    s = acceleration * radius / (4.0 * C_LIGHT**2)
    if s >= 1.0:
        raise ValueError("requested acceleration lies outside this weak static branch")
    return s / (1.0 - s)


def counterfactual_spherical_exterior_energy_j(
    *,
    scale_ev: float,
    source_radius_m: float,
    payload_center_m: float,
    payload_radius_m: float,
    target_acceleration_m_s2: float,
) -> dict[str, float]:
    """Bare exterior energy for the sign-flipped harmonic target.

    The source is a sphere of radius R_s. The payload center lies a distance d
    from the source center and has radius R_p. The scalar vacuum profile is

        Y(r) = K/r^4.

    K is chosen so the far payload surface reaches the target radial
    acceleration. For d>R_p, this is also the weakest outward axial component
    on the spherical payload for this r^-5 acceleration profile.

    The returned energy is only the canonical exterior scalar-gradient energy
    from R_s to infinity. It is not a complete source or operating energy.
    """
    source_radius = float(source_radius_m)
    payload_center = float(payload_center_m)
    payload_radius = float(payload_radius_m)
    target = float(target_acceleration_m_s2)

    if source_radius <= 0.0 or payload_radius <= 0.0:
        raise ValueError("source and payload radii must be positive")
    if payload_center <= source_radius + payload_radius:
        raise ValueError("source and payload must not intersect")
    if target <= 0.0:
        raise ValueError("target acceleration must be positive")

    far_radius = payload_center + payload_radius
    y_far = sign_flipped_required_y_at_radius(target, far_radius)
    k_m4 = y_far * far_radius**4
    y_source_surface = k_m4 / source_radius**4

    if y_source_surface >= 1.0:
        raise ValueError("profile crosses the declared invertibility domain Y<1")

    rho_scale = ev4_energy_density_j_m3(scale_ev)
    exterior_energy = 4.0 * math.pi * rho_scale * k_m4 / source_radius

    return {
        "scale_ev": float(scale_ev),
        "source_radius_m": source_radius,
        "payload_center_m": payload_center,
        "payload_radius_m": payload_radius,
        "far_payload_radius_m": far_radius,
        "target_acceleration_m_s2": target,
        "y_far_payload": y_far,
        "y_source_surface": y_source_surface,
        "jacobian_kinetic_eigenvalue_min": 1.0 - y_source_surface**2,
        "exterior_scalar_energy_j": exterior_energy,
    }


def scale_ev_for_counterfactual_energy(
    *,
    target_energy_j: float,
    source_radius_m: float,
    payload_center_m: float,
    payload_radius_m: float,
    target_acceleration_m_s2: float,
) -> float:
    """Invert the M^4 scaling of the counterfactual exterior-energy diagnostic."""
    energy = float(target_energy_j)
    if energy <= 0.0:
        raise ValueError("target_energy_j must be positive")
    unit = counterfactual_spherical_exterior_energy_j(
        scale_ev=1.0,
        source_radius_m=source_radius_m,
        payload_center_m=payload_center_m,
        payload_radius_m=payload_radius_m,
        target_acceleration_m_s2=target_acceleration_m_s2,
    )["exterior_scalar_energy_j"]
    return (energy / unit) ** 0.25
