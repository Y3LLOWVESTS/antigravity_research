"""032V17 C1 operator matching and finite-payload multipole diagnostics.

This module keeps three logically separate objects apart:

1. the published shift-symmetric j=0 operator coefficient C1;
2. the exact linear matter-loading solution inside a finite spherical payload;
3. a leading-log quantum-control diagnostic for the axial source EFT.

None of the helpers below constitutes a complete UV matching or a complete
operating-energy ledger.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.special import eval_legendre


C_LIGHT = 299792458.0

_POLY_CACHE: dict[int, list[dict[tuple[int, int], float]]] = {}


def c1_from_metric_scale_ev(metric_scale_ev: float) -> float:
    """Return C1=1/(2 M^4) in eV^-4 for the linearized conformal match."""
    scale = float(metric_scale_ev)
    if scale <= 0.0:
        raise ValueError("metric_scale_ev must be positive")
    return 1.0 / (2.0 * scale**4)


def jiang_nda_scale_from_c1_ev(c1_ev_m4: float) -> float:
    """Return Lambda=(16 pi^2/|C1|)^(1/4) in the Jiang et al. convention."""
    coefficient = abs(float(c1_ev_m4))
    if coefficient <= 0.0:
        raise ValueError("C1 must be nonzero")
    return (16.0 * math.pi**2 / coefficient) ** 0.25


def static_outward_metric_sign_from_c1(c1_ev_m4: float) -> bool:
    """Check the static sign for A=1-C1 (d phi)^2.

    With signature (+---), a static field has

        (d phi)^2 = -|grad phi|^2.

    Hence C1>0 gives

        A = 1 + C1 |grad phi|^2,

    which is the V13-V16 outward-sign target for a localized gradient whose
    magnitude decreases away from the source.
    """
    return float(c1_ev_m4) > 0.0


def corrected_laue_trace_support_floor_j(
    *,
    fermion_mean_pressure_inventory_j: float,
    scalar_field_energy_j: float,
) -> float:
    """Return isotropic Laue/DEC trace support lower bound.

    For a canonical static scalar,

        integral T^i_i dV = -E_phi.

    Therefore its contribution to the mean integrated pressure is -E_phi/3,
    not -E_phi. A compensating positive-energy support sector obeying DEC must
    carry at least the magnitude of the remaining mean integrated pressure.

    This remains a lower bound, not a constructed support solution.
    """
    pressure = float(fermion_mean_pressure_inventory_j)
    field = float(scalar_field_energy_j)
    return abs(pressure - field / 3.0)


def axial_leading_log_wavefunction_proxy(
    *,
    loop_proxy: float,
    cutoff_ev: float,
    mass_ev: float,
) -> float:
    """Return the declared fixed-order axial wavefunction-running proxy.

    Using the V16 loop variable

        L = N_f m^2/(4 pi^2 f^2),

    the convention-matched leading-log diagnostic is

        Delta Z_LL = 2 L log(Lambda^2/m^2).

    It is a perturbative-control diagnostic only. It is not a renormalized
    physical Z and must not be multiplied blindly into the operating energy.
    """
    loop = float(loop_proxy)
    cutoff = float(cutoff_ev)
    mass = float(mass_ev)

    if loop < 0.0 or cutoff <= 0.0 or mass <= 0.0:
        raise ValueError("invalid leading-log input")

    if cutoff <= mass:
        raise ValueError("cutoff must exceed mass for this running proxy")

    return 2.0 * loop * math.log((cutoff / mass) ** 2)


def _surface_nodes(
    *,
    a_m: float,
    c_m: float,
    n_t: int,
    n_phi: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return spheroid surface nodes and oriented scalar-source measure."""
    a = float(a_m)
    c = float(c_m)

    if a <= 0.0 or c <= 0.0:
        raise ValueError("source semi axes must be positive")

    t, weights_t = np.polynomial.legendre.leggauss(int(n_t))
    phi = np.linspace(0.0, 2.0 * math.pi, int(n_phi), endpoint=False)
    weight_phi = 2.0 * math.pi / int(n_phi)

    sin_theta = np.sqrt(np.maximum(0.0, 1.0 - t**2))

    tt = np.repeat(t, int(n_phi))
    ss = np.repeat(sin_theta, int(n_phi))
    pp = np.tile(phi, int(n_t))
    ww = np.repeat(weights_t, int(n_phi)) * weight_phi

    source = np.stack(
        (
            a * ss * np.cos(pp),
            a * ss * np.sin(pp),
            -c + c * tt,
        ),
        axis=1,
    )

    oriented_measure = a**2 * tt * ww

    return source, oriented_measure


def spheroid_incident_legendre_coefficients(
    *,
    a_m: float,
    c_m: float,
    payload_center_z_m: float,
    fit_radius_m: float,
    lmax: int = 20,
    n_t: int = 56,
    n_phi: int = 84,
    fit_order: int = 180,
) -> np.ndarray:
    """Expand the source potential as regular solid harmonics at the payload.

    The unit-polarization potential convention is chosen so that its gradient
    reproduces the V15 spheroid surface kernel.
    """
    center = float(payload_center_z_m)
    fit_radius = float(fit_radius_m)

    if center <= 0.0 or fit_radius <= 0.0:
        raise ValueError("invalid payload expansion geometry")

    source, measure = _surface_nodes(
        a_m=a_m,
        c_m=c_m,
        n_t=n_t,
        n_phi=n_phi,
    )

    u, weights = np.polynomial.legendre.leggauss(int(fit_order))

    potentials = np.zeros_like(u)

    for index, cosine in enumerate(u):
        rho = fit_radius * math.sqrt(max(0.0, 1.0 - cosine**2))
        point = np.array(
            [
                rho,
                0.0,
                center + fit_radius * cosine,
            ],
            dtype=float,
        )

        displacement = point - source
        radius = np.sqrt(np.sum(displacement**2, axis=1))

        potentials[index] = -float(
            np.sum(
                measure
                / (4.0 * math.pi * radius)
            )
        )

    coefficients = np.zeros(int(lmax) + 1, dtype=float)

    for ell in range(int(lmax) + 1):
        coefficients[ell] = (
            (2.0 * ell + 1.0)
            / 2.0
            * float(
                np.sum(
                    weights
                    * potentials
                    * eval_legendre(ell, u)
                )
            )
            / fit_radius**ell
        )

    return coefficients


def payload_transmission_factor(
    ell: int,
    epsilon_trace_load: float,
) -> float:
    """Return exact linear spherical-inclusion transmission factor T_l.

    The scalar kinetic coefficient inside the uniform payload is

        kappa = 1 + epsilon.

    Matching phi and kappa times its normal derivative gives

        T_l = (2l+1)/(l+1+kappa*l).
    """
    l_value = int(ell)
    epsilon = float(epsilon_trace_load)

    if l_value < 0 or epsilon < 0.0:
        raise ValueError("invalid multipole or trace load")

    if l_value == 0:
        return 1.0

    kappa = 1.0 + epsilon

    return (
        (2.0 * l_value + 1.0)
        / (
            l_value + 1.0
            + kappa * l_value
        )
    )


def _poly_add(
    first: dict[tuple[int, int], float],
    second: dict[tuple[int, int], float],
    first_scale: float,
    second_scale: float,
) -> dict[tuple[int, int], float]:
    result: dict[tuple[int, int], float] = {}

    for key, value in first.items():
        result[key] = result.get(key, 0.0) + first_scale * value

    for key, value in second.items():
        result[key] = result.get(key, 0.0) + second_scale * value

    return {
        key: value
        for key, value in result.items()
        if abs(value) > 1.0e-15
    }


def _multiply_z(
    polynomial: dict[tuple[int, int], float],
) -> dict[tuple[int, int], float]:
    return {
        (power_s, power_z + 1): value
        for (power_s, power_z), value in polynomial.items()
    }


def _multiply_r2(
    polynomial: dict[tuple[int, int], float],
) -> dict[tuple[int, int], float]:
    result: dict[tuple[int, int], float] = {}

    for (power_s, power_z), value in polynomial.items():
        result[(power_s + 1, power_z)] = (
            result.get((power_s + 1, power_z), 0.0)
            + value
        )

        result[(power_s, power_z + 2)] = (
            result.get((power_s, power_z + 2), 0.0)
            + value
        )

    return result


def _solid_harmonic_polynomials(
    lmax: int,
) -> list[dict[tuple[int, int], float]]:
    maximum = int(lmax)

    if maximum in _POLY_CACHE:
        return _POLY_CACHE[maximum]

    harmonics: list[dict[tuple[int, int], float]] = [
        {(0, 0): 1.0}
    ]

    if maximum >= 1:
        harmonics.append(
            {(0, 1): 1.0}
        )

    for ell in range(1, maximum):
        next_polynomial = _poly_add(
            _multiply_z(harmonics[ell]),
            _multiply_r2(harmonics[ell - 1]),
            (2.0 * ell + 1.0) / (ell + 1.0),
            -ell / (ell + 1.0),
        )

        harmonics.append(next_polynomial)

    _POLY_CACHE[maximum] = harmonics

    return harmonics


def _poly_derivatives(
    polynomial: dict[tuple[int, int], float],
    rho_m: float,
    z_m: float,
) -> tuple[float, float, float, float, float]:
    rho = float(rho_m)
    z = float(z_m)
    s = rho**2

    value = 0.0
    derivative_rho = 0.0
    derivative_z = 0.0
    derivative_rho_z = 0.0
    derivative_z_z = 0.0

    for (power_s, power_z), coefficient in polynomial.items():
        s_term = s**power_s if power_s else 1.0
        z_term = z**power_z if power_z else 1.0

        value += coefficient * s_term * z_term

        if power_s >= 1:
            derivative_rho += (
                coefficient
                * 2.0
                * rho
                * power_s
                * s**(power_s - 1)
                * z_term
            )

        if power_z >= 1:
            derivative_z += (
                coefficient
                * power_z
                * s_term
                * (
                    z**(power_z - 1)
                    if power_z > 1
                    else 1.0
                )
            )

        if power_s >= 1 and power_z >= 1:
            derivative_rho_z += (
                coefficient
                * 2.0
                * rho
                * power_s
                * power_z
                * s**(power_s - 1)
                * (
                    z**(power_z - 1)
                    if power_z > 1
                    else 1.0
                )
            )

        if power_z >= 2:
            derivative_z_z += (
                coefficient
                * power_z
                * (power_z - 1)
                * s_term
                * (
                    z**(power_z - 2)
                    if power_z > 2
                    else 1.0
                )
            )

    return (
        value,
        derivative_rho,
        derivative_z,
        derivative_rho_z,
        derivative_z_z,
    )


def transmitted_potential_derivatives(
    *,
    coefficients: np.ndarray,
    epsilon_trace_load: float,
    rho_m: float,
    z_relative_payload_center_m: float,
) -> tuple[float, float, float, float, float]:
    """Return potential, rho/z gradient, and rho-z/z-z Hessian entries."""
    coeff = np.asarray(coefficients, dtype=float)
    harmonics = _solid_harmonic_polynomials(len(coeff) - 1)

    result = np.zeros(5, dtype=float)

    for ell, coefficient in enumerate(coeff):
        transmission = payload_transmission_factor(
            ell,
            epsilon_trace_load,
        )

        result += (
            coefficient
            * transmission
            * np.asarray(
                _poly_derivatives(
                    harmonics[ell],
                    rho_m,
                    z_relative_payload_center_m,
                ),
                dtype=float,
            )
        )

    return tuple(float(value) for value in result)


def _local_acceleration_coefficients(
    *,
    coefficients: np.ndarray,
    epsilon_trace_load: float,
    rho_m: float,
    z_relative_payload_center_m: float,
) -> tuple[float, float]:
    _, grad_rho, grad_z, hessian_rho_z, hessian_z_z = (
        transmitted_potential_derivatives(
            coefficients=coefficients,
            epsilon_trace_load=epsilon_trace_load,
            rho_m=rho_m,
            z_relative_payload_center_m=z_relative_payload_center_m,
        )
    )

    linear_kernel = (
        -C_LIGHT**2
        * (
            grad_rho * hessian_rho_z
            + grad_z * hessian_z_z
        )
    )

    y_kernel = 0.5 * (
        grad_rho**2
        + grad_z**2
    )

    return linear_kernel, y_kernel


def required_q2_for_payload_surface(
    *,
    coefficients: np.ndarray,
    epsilon_trace_load: float,
    payload_radius_m: float,
    target_acceleration_m_s2: float,
    surface_count: int = 1201,
) -> dict[str, float]:
    """Return minimum q^2 making every payload-surface point outward >= target."""
    radius = float(payload_radius_m)
    target = float(target_acceleration_m_s2)

    if radius <= 0.0 or target <= 0.0:
        raise ValueError("invalid payload requirement")

    maximum_required = 0.0
    limiting_u = 0.0

    for cosine in np.linspace(-1.0, 1.0, int(surface_count)):
        rho = radius * math.sqrt(max(0.0, 1.0 - cosine**2))
        z_relative = radius * cosine

        linear_kernel, y_kernel = _local_acceleration_coefficients(
            coefficients=coefficients,
            epsilon_trace_load=epsilon_trace_load,
            rho_m=rho,
            z_relative_payload_center_m=z_relative,
        )

        denominator = linear_kernel - target * y_kernel

        if denominator <= 0.0:
            return {
                "q2": math.inf,
                "limiting_surface_cosine": float(cosine),
            }

        required = target / denominator

        if required > maximum_required:
            maximum_required = required
            limiting_u = float(cosine)

    return {
        "q2": maximum_required,
        "limiting_surface_cosine": limiting_u,
    }


def payload_surface_acceleration_metrics(
    *,
    coefficients: np.ndarray,
    epsilon_trace_load: float,
    payload_radius_m: float,
    q2: float,
    surface_count: int = 1201,
) -> dict[str, float]:
    """Return surface minimum, maximum, and nonuniformity."""
    radius = float(payload_radius_m)
    q_squared = float(q2)

    values: list[float] = []

    for cosine in np.linspace(-1.0, 1.0, int(surface_count)):
        rho = radius * math.sqrt(max(0.0, 1.0 - cosine**2))
        z_relative = radius * cosine

        linear_kernel, y_kernel = _local_acceleration_coefficients(
            coefficients=coefficients,
            epsilon_trace_load=epsilon_trace_load,
            rho_m=rho,
            z_relative_payload_center_m=z_relative,
        )

        values.append(
            linear_kernel
            * q_squared
            / (
                1.0
                + y_kernel * q_squared
            )
        )

    minimum = min(values)
    maximum = max(values)

    return {
        "surface_min_m_s2": minimum,
        "surface_max_m_s2": maximum,
        "surface_nonuniformity": maximum / minimum,
    }


def payload_volume_average_acceleration_m_s2(
    *,
    coefficients: np.ndarray,
    epsilon_trace_load: float,
    payload_radius_m: float,
    q2: float,
    order: int = 24,
) -> float:
    """Return spherical-payload volume-average +z acceleration."""
    radius = float(payload_radius_m)
    q_squared = float(q2)

    radial_nodes, radial_weights = np.polynomial.legendre.leggauss(int(order))
    angular_nodes, angular_weights = np.polynomial.legendre.leggauss(int(order))

    local_radii = 0.5 * radius * (radial_nodes + 1.0)
    local_weights = 0.5 * radius * radial_weights

    integral = 0.0

    for local_radius, local_weight in zip(local_radii, local_weights):
        for cosine, angular_weight in zip(angular_nodes, angular_weights):
            rho = local_radius * math.sqrt(max(0.0, 1.0 - cosine**2))
            z_relative = local_radius * cosine

            linear_kernel, y_kernel = _local_acceleration_coefficients(
                coefficients=coefficients,
                epsilon_trace_load=epsilon_trace_load,
                rho_m=rho,
                z_relative_payload_center_m=z_relative,
            )

            acceleration = (
                linear_kernel
                * q_squared
                / (
                    1.0
                    + y_kernel * q_squared
                )
            )

            integral += (
                float(local_weight)
                * float(angular_weight)
                * local_radius**2
                * acceleration
            )

    return 3.0 * integral / (2.0 * radius**3)


def _legendre_derivative(
    ell: int,
    cosine: float,
) -> float:
    l_value = int(ell)
    u = float(cosine)

    if l_value == 0:
        return 0.0

    if abs(u - 1.0) < 1.0e-11:
        return l_value * (l_value + 1.0) / 2.0

    if abs(u + 1.0) < 1.0e-11:
        return (
            (-1.0) ** (l_value + 1)
            * l_value
            * (l_value + 1.0)
            / 2.0
        )

    p_l = float(eval_legendre(l_value, u))
    p_previous = float(eval_legendre(l_value - 1, u))

    return (
        l_value
        * (
            u * p_l
            - p_previous
        )
        / (
            u**2
            - 1.0
        )
    )


def induced_payload_scattered_gradient(
    *,
    coefficients: np.ndarray,
    epsilon_trace_load: float,
    payload_radius_m: float,
    rho_from_payload_center_m: float,
    z_from_payload_center_m: float,
) -> tuple[float, float]:
    """Return rho,z gradient of payload-induced scattered field outside sphere."""
    coeff = np.asarray(coefficients, dtype=float)
    payload_radius = float(payload_radius_m)
    rho = float(rho_from_payload_center_m)
    z = float(z_from_payload_center_m)

    r = math.hypot(rho, z)

    if r <= payload_radius:
        raise ValueError("scattered exterior field requested inside payload")

    u = z / r
    radial_sine = rho / r

    gradient_rho = 0.0
    gradient_z = 0.0

    for ell, incident in enumerate(coeff):
        transmission = payload_transmission_factor(
            ell,
            epsilon_trace_load,
        )

        scattered = (
            (transmission - 1.0)
            * incident
            * payload_radius**(2 * ell + 1)
        )

        if scattered == 0.0:
            continue

        p_l = float(eval_legendre(ell, u))
        derivative = _legendre_derivative(ell, u)
        common = scattered * r ** (-ell - 2)

        gradient_rho += (
            common
            * radial_sine
            * (
                -(ell + 1.0) * p_l
                - u * derivative
            )
        )

        gradient_z += (
            common
            * (
                -(ell + 1.0) * u * p_l
                + (1.0 - u**2) * derivative
            )
        )

    return gradient_rho, gradient_z


def source_feedback_metrics(
    *,
    coefficients: np.ndarray,
    epsilon_trace_load: float,
    payload_radius_m: float,
    payload_center_z_m: float,
    source_a_m: float,
    source_c_m: float,
    source_demag_z: float,
    surface_count: int = 401,
) -> dict[str, float]:
    """Return center and source-surface payload-reaction field ratios.

    The uniformly polarized ellipsoid has constant self-field magnitude N_z in
    the unit-polarization convention, so the induced gradient can be compared
    directly to N_z.
    """
    center_z_global = -float(source_c_m)
    center_gradient = induced_payload_scattered_gradient(
        coefficients=coefficients,
        epsilon_trace_load=epsilon_trace_load,
        payload_radius_m=payload_radius_m,
        rho_from_payload_center_m=0.0,
        z_from_payload_center_m=(
            center_z_global
            - float(payload_center_z_m)
        ),
    )

    center_ratio = (
        math.hypot(*center_gradient)
        / float(source_demag_z)
    )

    maximum_ratio = 0.0

    for cosine in np.linspace(-0.999999, 0.999999, int(surface_count)):
        rho = (
            float(source_a_m)
            * math.sqrt(max(0.0, 1.0 - cosine**2))
        )

        z_global = (
            -float(source_c_m)
            + float(source_c_m) * cosine
        )

        induced = induced_payload_scattered_gradient(
            coefficients=coefficients,
            epsilon_trace_load=epsilon_trace_load,
            payload_radius_m=payload_radius_m,
            rho_from_payload_center_m=rho,
            z_from_payload_center_m=(
                z_global
                - float(payload_center_z_m)
            ),
        )

        ratio = (
            math.hypot(*induced)
            / float(source_demag_z)
        )

        maximum_ratio = max(maximum_ratio, ratio)

    return {
        "source_center_feedback_ratio": center_ratio,
        "source_surface_max_feedback_ratio": maximum_ratio,
    }
