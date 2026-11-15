"""HOOK17-PH7: coupled kinetic health and spectral momentum audit.

PURPOSE
-------
Independently re-discretize PH6's reduced two-carrier, source-driven
neutral-matter action and derive the previously untested joint carrier
and neutral-body kinetic Hessian.

Do not optimize portal parameters or prescribed source configurations.

PHYSICAL ACTION SCOPE
---------------------
The inherited PH6 reduced action contains two transverse carrier
potentials, two phenomenological localized current oscillators, movable
source centers, and a smeared neutral packet.

Its universal-metric-inspired matter term is:

    L_m = -rho(x-Z)*F(P)*sqrt(1-V**2)
    F(P) = exp(alpha*P-beta*P**2)
    P = ub*Da-ua*Db

The neutral packet has one collective velocity V.

JOINT KINETIC HESSIAN
---------------------
Set h=sqrt(1-V**2), q_j=(-Db_j,Da_j).

The local carrier velocity Hessian is

    H_uu[j] = dx*(I-rho_j*h*Fpp_j*q_j*q_j.T)

The mixed carrier-neutral velocity derivative is

    H_uV[j] = dx*rho_j*(V/h)*Fp_j*q_j

The collective neutral velocity derivative is

    H_VV = dx*sum_j rho_j*F_j/h**3

where Fp=dF/dP, Fpp=d2F/dP2.

For positive carrier blocks define

    K_j = 1-rho_j*h*Fpp_j*|q_j|**2

The exact collective-velocity Schur complement is

    S = H_VV
        -dx*sum_j [
            rho_j**2*V**2*Fp_j**2*|q_j|**2
            /(h**2*K_j)
        ]

Both K_j>0 everywhere AND S>0 are needed for the positive joint
kinetic matrix in this restricted semidiscrete action.

This does not certify gauge constraints, full material modes,
gravitational modes, UV physics, or complete hyperbolicity.

INDEPENDENT SPATIAL CONTROL
---------------------------
PH6 uses a centered periodic difference. PH7 substitutes a real
skew-adjoint Fourier derivative everywhere PH6 calls its spatial
derivative, using a temporary scope that restores the original.

Thus PH7 changes the spatial discretization, not the continuum toy
action or the physical portal.

The even-grid Nyquist derivative is zero. Nonlinear collocation and
sampled source profiles still introduce translation defects.
Consequently, exact semidiscrete momentum conservation is NOT assumed.

A separate resolution study tests whether the original PH6
negative-quadratic-only impulse survives a continuum refinement.

STRICT CLAIM LIMIT
------------------
Source oscillators are phenomenological and infinite in the two
suppressed transverse directions. Earth, hull, support stress,
finite 3D source matter, full Ward/Noether, gravity and exterior
radiation are not modeled.

No whole-spacecraft lift, real 1g/1m standoff, complete B11-M6
signed cycle, or sub-10-MJ device is established.

006D is unreplaced. Frozen ALPHA-1 M5V remains untouched.
"""

from __future__ import annotations

from dataclasses import asdict, replace
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import math

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

from antigravity_research.agminer import (
    hook17_ph6_same_action_bridge as ph6
)


BRANCH = "032H17A12D1R3X3B17-PH7"

ARCHIVES = {
    "ph6_module": (
        "src/antigravity_research/agminer/"
        "hook17_ph6_same_action_bridge.py",
        "02c0681999f8dab2f7508ade1a9bb168d8d160f1a1125489d4ec7f3a276b57e9",
    ),
    "ph6_result": (
        "results/data/"
        "032h17_ph6_same_action_bridge_20261115T011930061817Z.json",
        "ad11d0ef66b32f5237e03a59533ce540a7be03280c141bc94aa5794777ff9a62",
    ),
    "m5v_module": (
        "src/antigravity_research/agminer/"
        "hook17_r3b_m5v_unified_exterior_action.py",
        "ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f",
    ),
}


def spectral_D(a, dx):
    """Real, periodic, skew-adjoint Fourier spatial derivative."""
    a = np.asarray(a, dtype=float)

    if (
        a.ndim != 1
        or len(a) < 4
        or len(a) % 2
        or not math.isfinite(dx)
        or dx <= 0
        or not np.all(np.isfinite(a))
    ):
        raise ValueError(
            "Require finite one-dimensional even real grid and dx>0"
        )

    k = 2 * np.pi * np.fft.fftfreq(len(a), d=dx)
    k[len(a) // 2] = 0.

    return np.fft.ifft(
        1j * k * np.fft.fft(a)
    ).real


def hessian_symbolic():
    """Check exact first and second derivatives of the common action."""
    ua, ub, V, ga, gb, rho, aa, bb = sp.symbols(
        "ua ub V ga gb rho alpha beta",
        real=True,
    )

    P = ub * ga - ua * gb
    F = sp.exp(aa * P - bb * P * P)
    h = sp.sqrt(1 - V * V)

    L = (ua * ua + ub * ub) / 2 - rho * h * F
    H = sp.hessian(L, [ua, ub, V])

    q = sp.Matrix([-gb, ga])
    Fp = F * (aa - 2 * bb * P)
    Fpp = F * ((aa - 2 * bb * P)**2 - 2 * bb)

    carrier = (
        sp.eye(2)
        - rho * h * Fpp * q * q.T
    )

    mixed = rho * V / h * Fp * q
    neutral = rho * F / h**3

    for i in range(2):
        for j in range(2):
            assert sp.simplify(
                H[i, j] - carrier[i, j]
            ) == 0

        assert sp.simplify(
            H[i, 2] - mixed[i]
        ) == 0

    assert sp.simplify(
        H[2, 2] - neutral
    ) == 0

    K = 1 - rho*h*Fpp*(ga*ga + gb*gb)

    expected_det = (
        K*neutral
        - rho*rho*V*V*Fp*Fp
        * (ga*ga + gb*gb)/(h*h)
    )

    assert sp.simplify(
        H.det() - expected_det
    ) == 0

    return {
        "local_joint_velocity_hessian": "PASS_EXACT",
        "single_cell_joint_determinant": "PASS_EXACT",
        "global_schur_identity":
            "BLOCK_DIAGONAL_FIELD_HESSIAN_EXACT_REDUCTION",
        "full_gauge_gravity_modes": "NOT_DERIVED",
    }


def health(spec, state):
    """Calculate joint velocity-Hessian signature of PH6's action."""
    d = ph6.state_data(state, spec)

    rho = d["rho"]
    F = d["F"]
    sigma_prime = d["spr"]

    h = d.get("h", d.get("lorentz_h"))
    V = float(d["V"])
    dx = spec.length / spec.n

    q2 = d["ga"]**2 + d["gb"]**2

    Fp = F * sigma_prime
    Fpp = F * (
        sigma_prime**2 - 2 * spec.beta
    )

    K = 1 - rho*h*Fpp*q2

    if spec.density_mass <= 0:
        return {
            "neutral_present": False,
            "K_min": float(np.min(K)),
            "S": None,
            "joint_positive": None,
        }

    if np.min(K) <= 0:
        return {
            "neutral_present": True,
            "K_min": float(np.min(K)),
            "S": None,
            "joint_positive": False,
        }

    Hvv = float(
        dx * np.sum(rho * F / h**3)
    )

    correction = float(
        dx * np.sum(
            rho*rho*V*V*Fp*Fp*q2
            / (h*h*K)
        )
    )

    S = Hvv - correction

    return {
        "neutral_present": True,
        "K_min": float(np.min(K)),
        "H_VV": Hvv,
        "nonlocal_coupling_subtraction": correction,
        "S": S,
        "joint_positive": bool(S > 0),
        "neutral_velocity": V,
    }


def frozen_K_pass_joint_fail_example():
    """Demonstrate that positive frozen K alone is insufficient."""
    rho = 1.
    V = .9
    F = 1.
    Fp = 1.
    Fpp = 1.
    q2 = 1.3

    h = math.sqrt(1 - V*V)

    K = 1 - rho*h*Fpp*q2
    Hvv = rho*F/h**3

    S = (
        Hvv
        - rho*rho*V*V*Fp*Fp*q2
        / (h*h*K)
    )

    if not (K > 0 and S < 0):
        raise AssertionError(
            "Expected frozen-K pass with joint-Hessian failure"
        )

    return {
        "frozen_K_positive": K,
        "joint_S_negative": S,
        "classification":
            "RED_JOINT_KINETIC_DESPITE_POSITIVE_FROZEN_K",
    }


def evolve_spectral(spec=None, samples=65):
    """Run action-consistent Fourier spatial control without resets."""
    if spec is None:
        spec = ph6.Spec()

    ph6.validate(spec)

    # Scope the alternate spatial derivative to one run.
    # Original PH6 functions and source files are never edited.
    with patch.object(ph6, "D", spectral_D):
        y0 = ph6.initial(spec)

        times = np.linspace(
            0, spec.tmax, samples
        )

        solution = solve_ivp(
            ph6.rhs,
            (0, spec.tmax),
            y0,
            args=(spec,),
            t_eval=times,
            method="DOP853",
            rtol=3e-9,
            atol=3e-11,
            max_step=.016,
        )

        if (
            not solution.success
            or not np.all(np.isfinite(solution.y))
        ):
            raise RuntimeError(
                "Spectral source evolution failed"
            )

        records = [
            ph6.diagnostics(
                solution.y[:, i], spec
            )
            for i in range(len(times))
        ]

        hessians = [
            health(
                spec, solution.y[:, i]
            )
            for i in range(len(times))
        ]

        forces = np.array([
            ph6.rhs(
                float(times[i]),
                solution.y[:, i],
                spec,
            )[4*spec.n+1]
            for i in range(len(times))
        ])

    E0 = records[0]["total_energy"]
    P0 = records[0]["total_momentum"]

    signed = float(
        np.trapezoid(forces, times)
    )

    positive = float(
        np.trapezoid(
            np.maximum(forces, 0), times
        )
    )

    negative = float(
        np.trapezoid(
            np.minimum(forces, 0), times
        )
    )

    dp = float(
        records[-1]["neutral_momentum"]
        - records[0]["neutral_momentum"]
    )

    return {
        "spec": asdict(spec),
        "initial": records[0],
        "final": records[-1],

        "neutral_signed_momentum_change": dp,
        "neutral_positive_integrated_force": positive,
        "neutral_negative_integrated_force": negative,
        "signed_force_integral": signed,

        "impulse_quadrature_discrepancy":
            abs(signed-dp),

        "max_energy_drift": max(
            abs(r["total_energy"]-E0)
            for r in records
        ),

        "max_momentum_drift": max(
            abs(r["total_momentum"]-P0)
            for r in records
        ),

        "min_frozen_K": min(
            r["K_min"] for r in hessians
        ),

        "min_full_S": (
            min(
                r["S"] for r in hessians
                if r["S"] is not None
            )
            if spec.density_mass > 0
            else None
        ),

        "full_joint_hessian_pass_all_times": (
            all(
                r["joint_positive"]
                for r in hessians
                if r["neutral_present"]
            )
            if spec.density_mass > 0
            else None
        ),

        "no_reset": True,
        "closed_cycle": False,
        "radiation_to_infinity":
            "NOT_MODELED_PERIODIC_DOMAIN",
        "full_source_microscopic": "NO",
        "earth_craft_lift": "NOT_DERIVED",
    }


def provenance(root: Path):
    """Read archived source and result hashes without modification."""
    result = {}

    for name, (relative, expected) in ARCHIVES.items():
        path = root / relative

        if not path.is_file():
            result[name] = {
                "status": "MISSING",
                "expected_sha256": expected,
            }
            continue

        actual = sha256(
            path.read_bytes()
        ).hexdigest()

        result[name] = {
            "status": (
                "MATCH"
                if actual == expected
                else "HASH_MISMATCH"
            ),
            "actual_sha256": actual,
            "expected_sha256": expected,
        }

    return result


def run(root: Path):
    """Pre-registered PH7 reproducibility and kinetic-health matrix."""
    exact = hessian_symbolic()
    counter = frozen_K_pass_joint_fail_example()

    baseline = ph6.Spec()

    series = {
        f"spectral_n{n}": evolve_spectral(
            replace(baseline, n=n)
        )
        for n in (128, 256, 384, 512)
    }

    fine = series["spectral_n512"]

    controls = {
        "portal_off": evolve_spectral(
            replace(
                baseline, n=256,
                alpha=0., beta=0.
            )
        ),

        "negative_even_only": evolve_spectral(
            replace(
                baseline, n=256,
                alpha=0.
            )
        ),

        "linear_only": evolve_spectral(
            replace(
                baseline, n=256,
                beta=0.
            )
        ),

        "neutral_absent": evolve_spectral(
            replace(
                baseline, n=256,
                density_mass=0.
            )
        ),

        "both_sources_off": evolve_spectral(
            replace(
                baseline, n=256,
                q0_x=0., q0_y=0.
            )
        ),
    }

    if not (
        fine["max_momentum_drift"] < 1e-6
        and fine["max_energy_drift"] < 1e-9
        and fine["neutral_signed_momentum_change"] > 0
        and all(
            c["full_joint_hessian_pass_all_times"]
            for c in series.values()
        )
        and abs(
            controls["portal_off"][
                "neutral_signed_momentum_change"
            ]
        ) < 1e-10
        and abs(
            controls["negative_even_only"][
                "neutral_signed_momentum_change"
            ]
        ) < 1e-8
        and controls["linear_only"][
            "neutral_signed_momentum_change"
        ] > 0
        and controls["neutral_absent"][
            "neutral_signed_momentum_change"
        ] == 0
        and abs(
            controls["both_sources_off"][
                "neutral_signed_momentum_change"
            ]
        ) < 1e-10
    ):
        raise AssertionError(
            "PH7 pre-registered controls failed"
        )

    dp256 = series["spectral_n256"][
        "neutral_signed_momentum_change"
    ]

    dp384 = series["spectral_n384"][
        "neutral_signed_momentum_change"
    ]

    dp512 = fine[
        "neutral_signed_momentum_change"
    ]

    if (
        abs(dp384-dp512) > 2e-5
        or abs(dp256-dp512) > 2e-4
    ):
        raise AssertionError(
            "Spectral neutral response not converged"
        )

    # Reproduce PH6's negative-even coarse-grid erratum.
    # Centered PH6 must be restored after spectral controls.
    centered_even = {
        f"centered_n{n}": ph6.run_case(
            replace(
                baseline, n=n,
                alpha=0.
            ),
            samples=65,
        )
        for n in (96, 128, 256, 384)
    }

    if not (
        abs(
            centered_even["centered_n96"][
                "neutral_exact_momentum_change"
            ]
        ) > 1e-6
        and abs(
            centered_even["centered_n384"][
                "neutral_exact_momentum_change"
            ]
        ) < 1e-9
    ):
        raise AssertionError(
            "PH6 negative-even erratum failed reproduction"
        )

    history = provenance(root)

    history_ok = all(
        item["status"] == "MATCH"
        for item in history.values()
    )

    neutral = fine["final"]["neutral_momentum"]
    field = fine["final"]["field_momentum"]
    source = fine["final"]["source_momentum"]

    return {
        "branch": BRANCH,
        "reference":
            "PH6_REDISCRETIZATION_ALPH A1_M5V_FROZEN".replace(
                "ALPH A1", "ALPHA1"
            ),
        "exact_coupled_hessian": exact,
        "kinetic_counterexample": counter,
        "archival_provenance": history,
        "spectral_resolution_series": series,
        "independent_controls": controls,

        "negative_even_coarse_grid_erratum": {
            key: float(
                value["neutral_exact_momentum_change"]
            )
            for key, value in centered_even.items()
        },

        "fine_momentum_ledger": {
            "neutral_momentum": neutral,
            "field_momentum": field,
            "source_center_momentum": source,
            "total_initial":
                fine["initial"]["total_momentum"],
            "total_final":
                fine["final"]["total_momentum"],
            "neutral_plus_field_plus_source":
                neutral+field+source,
        },

        "gates": {
            "P0_PH6_PROVENANCE": (
                "PASS" if history_ok
                else "UNRESOLVED"
            ),

            "P1_EXACT_JOINT_KINETIC_HESSIAN":
                "PASS_REDUCED_ACTION_SCOPED",

            "P1_FROZEN_K_SUFFICIENT":
                "NO_COUNTEREXAMPLE_ESTABLISHED",

            "P1_EVOLVED_JOINT_KINETIC":
                "PASS_SCOPED_SAMPLED_STATES",

            "P2_CROSS_DISCRETIZATION_IMPULSE":
                "PASS_REDUCED_NUMERICAL_SCREEN",

            "P2_MOMENTUM_LEDGER":
                "PASS_NUMERICAL_SCREEN_NOT_EXACT_NOETHER",

            "P2_PH6_NEGATIVE_EVEN_SIGNAL":
                "DEMOTED_GRID_ARTIFACT",

            "P2_COMPLETE_SIGNED_SOURCE_CYCLE":
                "NOT_RUN",

            "P3_FULL_GAUGE_WARD_SOURCE_EOM":
                "NOT_DERIVED",

            "P3_EARTH_DOWN_WHOLE_CRAFT_UP":
                "NOT_DERIVED",

            "B11_M6_COMPLETE_LOADED_IMPULSE":
                "NOT_RUN",

            "NEUTRAL_GE1G_AT_GE1M":
                "NOT_CERTIFIED",

            "STRICT_COMPLETE_LT10MJ":
                "NOT_CERTIFIED",

            "006D_REPLACED": "NO",
        },

        "verdict":
            "YELLOW_CROSS_DISCRETIZATION_AND_JOINT_KINETIC_NO_ENGINE",
    }
