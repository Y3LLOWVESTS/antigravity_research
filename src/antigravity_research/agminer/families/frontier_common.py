"""Shared Tier-0 physics utilities for AGMINER frontier families.

These routines calculate optimistic analytic lower bounds only.
A sub-threshold result is not a field solution or certification.
"""

from __future__ import annotations

import math
from typing import Any

MPL_REDUCED_GEV = 2.435e18
TOP_MASS_GEV = 172.76
HBARC_GEV_M = 1.973269804e-16
HBARC_EV_M = 1.973269804e-7
GEV_TO_J = 1.602176634e-10
C_LIGHT = 299792458.0


def alpha_value(params: dict[str, float]) -> float:
    return 10.0 ** float(params["log10_alpha"])


def cutoff_gev(params: dict[str, float]) -> float:
    return 10.0 ** float(params["log10_cutoff_gev"])


def range_m(params: dict[str, float]) -> float:
    return float(params["range_m"])


def mediator_mass_ev(params: dict[str, float]) -> float:
    return HBARC_EV_M / range_m(params)


def payload_volume_m3(config: dict[str, Any]) -> float:
    radius = float(config["payload_radius_m"])
    return 4.0 * math.pi * radius ** 3 / 3.0


def volume_gev_minus3(config: dict[str, Any]) -> float:
    return payload_volume_m3(config) / HBARC_GEV_M ** 3


def required_gradient_gev2(
    alpha: float,
    config: dict[str, Any],
) -> float:
    acceleration = float(config["target_cm_accel_mps2"])
    return (
        MPL_REDUCED_GEV
        / alpha
        * acceleration
        / C_LIGHT ** 2
        * HBARC_GEV_M
    )


def heavy_threshold_alpha_max(
    params: dict[str, float],
) -> float:
    mass_ev = mediator_mass_ev(params)
    cutoff = cutoff_gev(params)
    loop_mass_per_alpha_ev = (
        TOP_MASS_GEV
        * cutoff
        / (2.0 * math.pi * MPL_REDUCED_GEV)
        * 1.0e9
    )
    return mass_ev / loop_mass_per_alpha_ev


def twin_naturalness_gate(
    params: dict[str, float],
    config: dict[str, Any],
) -> dict[str, Any]:
    alpha = alpha_value(params)
    maximum = heavy_threshold_alpha_max(params)
    passed = alpha <= maximum
    return {
        "passed": passed,
        "failure_code": None if passed else "N001",
        "alpha": alpha,
        "alpha_max": maximum,
        "margin": maximum / alpha,
    }


def basic_eft_gate(
    params: dict[str, float],
    config: dict[str, Any],
    strong_scale_ev: float | None = None,
) -> dict[str, Any]:
    cutoff = cutoff_gev(params)
    mass_ev = mediator_mass_ev(params)
    radius = float(config["payload_radius_m"])
    length = min(radius, range_m(params))
    momentum_gev = HBARC_GEV_M / length
    passed = cutoff >= TOP_MASS_GEV

    if strong_scale_ev is not None:
        strong_scale_gev = strong_scale_ev * 1.0e-9
        passed = (
            passed
            and strong_scale_gev > 10.0 * momentum_gev
            and strong_scale_ev > 10.0 * mass_ev
        )

    return {
        "passed": passed,
        "failure_code": None if passed else "N002",
        "cutoff_gev": cutoff,
        "mediator_mass_ev": mass_ev,
        "probe_momentum_gev": momentum_gev,
    }


def canonical_payload_floor_j(
    alpha: float,
    config: dict[str, Any],
) -> float:
    gradient = required_gradient_gev2(alpha, config)
    energy_gev = (
        0.5
        * volume_gev_minus3(config)
        * gradient ** 2
    )
    return energy_gev * GEV_TO_J


def dbi_payload_floor_j(
    alpha: float,
    strong_scale_ev: float,
    config: dict[str, Any],
) -> float:
    gradient = required_gradient_gev2(alpha, config)
    scale_gev = strong_scale_ev * 1.0e-9
    x = gradient / scale_gev ** 2
    root = math.sqrt(1.0 + x * x)
    delta = x * x / (root + 1.0)
    rho_gev4 = scale_gev ** 4 * delta
    return (
        volume_gev_minus3(config)
        * rho_gev4
        * GEV_TO_J
    )


def polynomial_k_payload_floor_j(
    alpha: float,
    strong_scale_ev: float,
    config: dict[str, Any],
) -> float:
    gradient = required_gradient_gev2(alpha, config)
    scale_gev = strong_scale_ev * 1.0e-9
    rho_gev4 = (
        0.5 * gradient ** 2
        + 0.25 * gradient ** 4 / scale_gev ** 4
    )
    return (
        volume_gev_minus3(config)
        * rho_gev4
        * GEV_TO_J
    )

def projected_payload_area_gev_minus2(config: dict[str, Any]) -> float:
    radius = float(config["payload_radius_m"])
    return math.pi * (radius / HBARC_GEV_M) ** 2


def collective_naturalness_gate(
    params: dict[str, float],
    n_fields: int,
    config: dict[str, Any],
) -> dict[str, Any]:
    alpha_single = alpha_value(params)
    alpha_effective = alpha_single * math.sqrt(float(n_fields))
    alpha_max = heavy_threshold_alpha_max(params)
    passed = alpha_effective <= alpha_max
    return {
        "passed": passed,
        "failure_code": None if passed else "N001",
        "alpha_single": alpha_single,
        "alpha_effective": alpha_effective,
        "alpha_max": alpha_max,
    }


def canonical_collective_payload_floor_j(
    alpha: float,
    n_fields: int,
    config: dict[str, Any],
) -> float:
    alpha_effective = alpha * math.sqrt(float(n_fields))
    return canonical_payload_floor_j(alpha_effective, config)


def canonical_collective_source_floor_j(
    alpha: float,
    n_fields: int,
    config: dict[str, Any],
) -> float:
    n = float(n_fields)
    gradient_each = required_gradient_gev2(alpha * n, config)
    charge_each = (
        gradient_each
        * projected_payload_area_gev_minus2(config)
    )
    energy_each_j = (
        charge_each
        * MPL_REDUCED_GEV
        / alpha
        * GEV_TO_J
    )
    return energy_each_j


def collective_dbi_payload_floor_j(
    alpha: float,
    n_fields: int,
    strong_scale_ev: float,
    config: dict[str, Any],
) -> float:
    n = float(n_fields)
    gradient_each = required_gradient_gev2(alpha * n, config)
    scale_gev = strong_scale_ev * 1.0e-9
    x = gradient_each / scale_gev ** 2
    root = math.sqrt(1.0 + x * x)
    delta = x * x / (root + 1.0)
    rho_each_gev4 = scale_gev ** 4 * delta
    return (
        n
        * volume_gev_minus3(config)
        * rho_each_gev4
        * GEV_TO_J
    )


def collective_dbi_source_floor_j(
    alpha: float,
    n_fields: int,
    strong_scale_ev: float,
    config: dict[str, Any],
) -> float:
    n = float(n_fields)
    gradient_each = required_gradient_gev2(alpha * n, config)
    scale_gev = strong_scale_ev * 1.0e-9
    x = gradient_each / scale_gev ** 2
    displacement_each = (
        gradient_each
        / math.sqrt(1.0 + x * x)
    )
    charge_each = (
        displacement_each
        * projected_payload_area_gev_minus2(config)
    )
    energy_each_j = (
        charge_each
        * MPL_REDUCED_GEV
        / alpha
        * GEV_TO_J
    )
    return energy_each_j
