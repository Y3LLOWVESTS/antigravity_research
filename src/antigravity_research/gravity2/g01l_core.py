"""GRAVITY2 G01-L: two-sided Maxwell and worldvolume stress audit.

SCIENTIFIC QUESTION
-------------------
Does the G01-K quadratic shell reduction follow from regular,
two-sided, source-free bulk Maxwell X/Y fields and the declared
closed spherical worldvolume action?

MODEL
-----
Sigma = R_t x S2, f=da, with no magnetic monopole sheet.

Bulk:
    -1/2 integral (F_X wedge *F_X + F_Y wedge *F_Y)

Worldvolume:
    integral [
        A_X wedge f
        - K/2 f wedge *3 f
        - g f wedge *3 pullback(F_Y)
        - H/2 pullback(F_Y) wedge *3 pullback(F_Y)
    ]

The full source, support, Einstein and physical-metric actions
are NOT supplied by G01-K. This implementation does not invent
them or treat them as demonstrated.

ASSUMPTIONS
-----------
The interior and exterior Y fields satisfy source-free Maxwell
equations away from the interface. Nonzero normal magnetic
flux is continuous across the shell.

The calculated interior coefficient R/ell is conditional on
that source-free, regular interior. New bulk source matter
would require an independently derived different action.

ENERGY
------
K, g, H, magnetic mode energies and drives are canonical
model quantities. They are not certified SI material data.

CLAIMS
------
A passed numerical check is a necessary-condition audit,
not physical gravity, spacecraft propulsion or an engine.
"""
from __future__ import annotations

from fractions import Fraction
import math

import numpy as np

CAPACITY = 1.5429162116460216
HISTORICAL_INWARD = -129.67185782242464

PARENTS = {
    "G01K_SCIENCE": (
        "results/gravity2/g01k_runs/"
        "g01k_20261121T214747Z_7aba9bce/science.json",
        "3e81c419afd30d416cb440383ff700a81750f1188383c38ff34732900ae75b12",
    ),
    "G01J_SCIENCE": (
        "results/gravity2/g01j_bf_runs/"
        "g01jbf_20261121T213657Z_282a797e/science.json",
        "ce57c05c45428548afe80175943cc256fac94212cbc1b0415ff8a73f6dbd6ce3",
    ),
    "G01K_SOURCE": (
        "scripts/g01k_source_v1.py",
        "cb6bc822e2dd363c48982f677c7d852317392098e4e7f610f3506e68e9468112",
    ),
}


def full_mode(ell: int, radius: float) -> dict:
    """Exact regular spherical harmonic Maxwell kernels.

    X: electrostatic surface charge q.
    Y: normal magnetic field b.

    Both bulk domains have ordinary source-free Maxwell
    equations away from the material interface.

    Coefficients multiply the same surface-mode L2 weight
    used by the G01-J and G01-K parent calculations.
    """
    if not isinstance(ell, int) or ell < 1 or radius <= 0:
        raise ValueError("INVALID_SPHERICAL_MODE")

    e = Fraction(ell)
    r = Fraction(str(radius))

    x_external = r * (e + 1) / (2 * e + 1)**2
    x_internal = r * e / (2 * e + 1)**2

    y_external = r / (e + 1)
    y_internal = r / e

    return {
        "X_exterior": float(x_external),
        "X_interior": float(x_internal),
        "X_full": float(x_external + x_internal),
        "Y_exterior": float(y_external),
        "Y_interior": float(y_internal),
        "Y_full": float(y_external + y_internal),
    }


def radial_midpoint_error(ell: int, n: int) -> float:
    """Radial finite-volume quadrature after u=R/r mapping.

    For each source-free magnetic multipole, the relevant
    normalized radial integral is

        (2*ell+1) integral_0^1 u^(2*ell) du = 1.

    This provides a convergence check independent of
    merely evaluating the rational field-energy formula.
    """
    u = (np.arange(n, dtype=float) + 0.5) / n

    return abs(
        float(
            (2 * ell + 1)
            * np.mean(u ** (2 * ell))
            - 1
        )
    )


def stress_tensor(h, f, y, K, coupling, H):
    """Exact induced-metric Hilbert tensor for Hodge terms.

    h is a 2+1 Lorentzian covariant metric.
    f and y are fixed covariant antisymmetric two-forms.

    The BF term A_X wedge f has zero direct Hilbert
    stress. The K, g and H terms do NOT generally vanish.
    """
    h = np.array(h, dtype=float)
    f = np.array(f, dtype=float)
    y = np.array(y, dtype=float)

    inv = np.linalg.inv(h)

    ff = float(np.sum(f * (inv @ f @ inv.T)))
    fy = float(np.sum(f * (inv @ y @ inv.T)))
    yy = float(np.sum(y * (inv @ y @ inv.T)))

    return (
        K * (
            f @ inv @ f.T
            - 0.25 * h * ff
        )
        + coupling * (
            f @ inv @ y.T
            + y @ inv @ f.T
            - 0.5 * h * fy
        )
        + H * (
            y @ inv @ y.T
            - 0.25 * h * yy
        )
    )


def metric_witness() -> dict:
    """Nontrivial Lorentzian test with electric/magnetic terms."""
    h = np.diag([-1.0, 1.6, 2.1])

    f = np.array([
        [0.0, 0.3, -0.4],
        [-0.3, 0.0, 0.7],
        [0.4, -0.7, 0.0],
    ])

    y = np.array([
        [0.0, -0.2, 0.25],
        [0.2, 0.0, 0.6],
        [-0.25, -0.6, 0.0],
    ])

    T = stress_tensor(h, f, y, 2.0, 4.0, 8.2)
    T_no_H = stress_tensor(h, f, y, 2.0, 4.0, 0.0)
    T_no_g = stress_tensor(h, f, y, 2.0, 0.0, 8.2)

    return {
        "h": h.tolist(),
        "f": f.tolist(),
        "Y": y.tolist(),
        "kinetic_T_ab": T.tolist(),
        "BF_direct_Hilbert_T_ab": "EXACT_ZERO",
        "omit_H_changes_T": bool(
            np.max(np.abs(T - T_no_H)) > 1e-3
        ),
        "omit_mixed_Hodge_changes_T": bool(
            np.max(np.abs(T - T_no_g)) > 1e-3
        ),
    }


def compute(k: dict, j: dict) -> dict:
    """Evaluate the G01-K action-reduction necessary conditions."""
    R = float(k["source_radius_m"])

    if R != 2.0 or float(j["source_radius_m"]) != R:
        raise ValueError("PARENT_RADIUS_DRIFT")

    K = R
    coupling = 2 * R
    H = 4.1 * R

    rows = []
    max_target_error = 0.0
    total_interior_proxy = 0.0
    max_quad_error = 0.0

    for old, mode in zip(k["modes"], j["modes"]):
        ell = int(mode["ell"])

        if ell != old["ell"] or ell != len(rows) + 1:
            raise ValueError("MODE_INDEX_DRIFT")

        b = float(mode["b_mode"])
        weight = float(mode["basis_l2_area_weight"])

        if not math.isfinite(b) or weight <= 0:
            raise ValueError("INVALID_MODE_INPUT")

        kernels = full_mode(ell, R)

        A = kernels["X_full"]
        Mext = kernels["Y_exterior"]
        Mint = kernels["Y_interior"]
        Mfull = kernels["Y_full"]

        if (
            abs(A - old["A_electrostatic"]) > 1e-12
            or abs(
                Mext - old["M_magnetic_exterior"]
            ) > 1e-12
        ):
            raise ValueError("PARENT_DTN_OPERATOR_DRIFT")

        # This response can remain algebraically exact
        # even after restoring the interior magnetic energy.
        q = -coupling * b / (K + A)

        if not math.isclose(
            q,
            old["required_q"],
            rel_tol=3e-13,
            abs_tol=3e-13,
        ):
            raise ValueError(
                "ORIGINAL_SPECTRAL_RESPONSE_NOT_PRESERVED"
            )

        old_drive = (H + Mext) * b + coupling * q
        full_drive = (H + Mfull) * b + coupling * q

        if not math.isclose(
            old_drive,
            old["required_drive_J_canonical"],
            rel_tol=2e-12,
            abs_tol=2e-12,
        ):
            raise ValueError("PARENT_DRIVE_DRIFT")

        old_det = (K + A) * (H + Mext) - coupling**2
        full_det = (K + A) * (H + Mfull) - coupling**2

        quad = [
            radial_midpoint_error(ell, n)
            for n in (128, 256, 512, 1024)
        ]

        if not (
            full_det > old_det > 0
            and quad[-1] < quad[0]
            and all(
                x > y for x, y in zip(quad, quad[1:])
            )
        ):
            raise ValueError(
                "PHYSICAL_ENERGY_OR_QUADRATURE_FAIL"
            )

        correction = 0.5 * weight * Mint * b * b

        total_interior_proxy += correction
        max_quad_error = max(max_quad_error, quad[-1])

        max_target_error = max(
            max_target_error,
            abs(q - old["required_q"])
            / max(1.0, abs(old["required_q"])),
        )

        rows.append({
            "ell": ell,
            "b_mode": b,
            "q_mode": q,
            "weight": weight,
            **kernels,
            "old_drive": old_drive,
            "required_two_sided_drive": full_drive,
            "delta_drive": Mint * b,
            "old_hessian_determinant": old_det,
            "full_hessian_determinant": full_det,
            "old_magnetic_energy_proxy":
                0.5 * weight * Mext * b * b,
            "mandatory_interior_magnetic_energy_proxy":
                correction,
            "radial_midpoint_errors": quad,
            "magnetic_normal_continuity":
                "B_normal_plus_equals_B_normal_minus",
            "zero_interior_with_nonzero_Bnormal":
                "FORBIDDEN_BY_dF_Y_EQUALS_ZERO",
        })

    return {
        "schema":
            "gravity2.g01l.two_sided_shell_variation.v1",
        "status":
            "ACTION_INCOMPLETE_G01K_EXTERIOR_ONLY_KERNEL_NOT_FULL_TWO_SIDED_MAXWELL",
        "claim":
            "SCOPED_NECESSARY_MAXWELL_BOUNDARY_CORRECTION_NOT_GRAVITY",
        "parent_shas": {
            name: value[1]
            for name, value in PARENTS.items()
        },
        "canonical_radius": R,
        "K": K,
        "g": coupling,
        "H": H,
        "action":
            "Maxwell_4D_X_Y + BF_AX_wedge_da + "
            "shell_K_f2 + shell_g_fFY + shell_H_FY2; "
            "source/support/EH/metric not fully specified",
        "shell_a_variation":
            "d(K star3 f + g star3 pullback(FY) - AX)=0",
        "X_interface_variation":
            "j_X_dual_2form=f=da; d f=0",
        "Y_interface_variation":
            "surface current 2form = "
            "d(g star3 f + H star3 pullback(FY)); "
            "orientation-fixed bulk jump required",
        "Ward":
            "closed_S2_BF_gauge_invariant_up_to_boundary; "
            "edge_inflow_unresolved",
        "magnetic_bianchi":
            "dF_Y=0 -> Bnormal_plus=Bnormal_minus; "
            "no_monopoles",
        "metric_stress": metric_witness(),
        "modes": rows,
        "total_mandatory_interior_magnetic_energy_proxy":
            total_interior_proxy,
        "max_1024_radial_relative_error":
            max_quad_error,
        "max_charge_reconstruction_error":
            max_target_error,
        "current_energy_scope":
            "CANONICAL_PROXY_NOT_SI_JOULES",
        "magnetic_drive":
            "REQUIRED_NOT_ONSHELL_SOURCED",
        "complete_4D_shell_embedding_variation":
            "NOT_DERIVED",
        "microscopic_Y_current_and_support":
            "NOT_DERIVED",
        "universal_metric_and_Einstein_variations":
            "NOT_DERIVED",
        "neutral_matter_loaded_sign":
            "HISTORICAL_INWARD_FAILURE_UNRESOLVED",
        "Earth_down_craft_up":
            "NOT_DERIVED",
        "complete_operating_energy":
            "NOT_CERTIFIED",
        "R3B_prescribed_capacity_J": CAPACITY,
        "historical_loaded_acceleration_m_s2":
            HISTORICAL_INWARD,
        "physical_survivors": 0,
        "replaced_006D": False,
        "first_failed_gate":
            "TWO_SIDED_MAXWELL_Y_INTERIOR_OMITTED_FROM_G01K_REDUCED_KERNEL",
        "next_authorization":
            "G01M_ONLY_AFTER_NEW_COMPLETE_SOURCE_AND_INTERIOR_BOUNDARY_ACTION",
    }
