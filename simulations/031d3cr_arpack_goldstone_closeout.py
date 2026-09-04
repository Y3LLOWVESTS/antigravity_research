"""
031D3C
======

Coupled-linear stability and Q_Y switching/resource gate for the promoted
031D3B microscopic activation field.

Inherited GREEN results
-----------------------
031D3B established a static microscopic ON solution containing

    X Q-ball source
    scalar phi
    activation Q-ball Y

with both global charges Q_X and Q_Y fixed.

The 031C/D96 source X+phi subsystem has already passed an independent
coupled-linear l=0..8 certification including the l=1 translational
Goldstone diagnosis.

D3C asks what the new activation field changes dynamically.

Physical coupling
-----------------

    f(a) = 1-exp(-a^2/2)

    A = exp[-f(a) u^2/2]

The canonical second-variation fields are:

    X amplitude
    X phase
    scalar u/chi
    Y amplitude sqrt(rho_Y) a
    Y phase     sqrt(rho_Y) phase_Y

The exact local Hessian entries used here are derived from

    V =
        A(u,a) W_X(y)
        + epsilon^2 u^2/(2 chi^2)
        + rho_Y mu^2 W_Y(a)

with

    W(q)=1/2 log(1+q^2).

For each angular harmonic l, use the radial-reduced fields r delta-field.

Dynamic rotating-frame system:

    q_tt + G q_t + K q = 0

with gyroscopic blocks

    G_X:
        +2 Omega_X
        -2 Omega_X

and

    G_Y:
        +2 mu Omega_Y
        -2 mu Omega_Y.

The quadratic problem

    (s^2 I + s G + K) q = 0

is converted to first order.

Symmetries
----------
Two exact global U(1) phase modes exist in l=0.

One exact common translational Goldstone mode exists in l=1.

The relative X/phi versus Y translation is NOT an exact symmetry and is
therefore retained as a physical mode.

A positive-growth mode is never discarded merely because it lies in l=1.
Only strong overlap with the analytic common-translation mode can classify
the known discretized Goldstone artifact.

Numerical strategy
------------------
Use large physical boxes because Y is much broader than X.

Broad spectra:
    Rmax = 600 in x=m_X r
    h = 0.50 and 0.375
    l=0..8

Extra l=1:
    Rmax=600, h=0.25
    Rmax=800, h=0.50

Both near-zero shift-invert modes and rightmost modes are requested.

Failure of ARPACK is numerical incompleteness, not stability evidence.

Switching
---------
ON has Q_Y != 0.

Exact vacuum OFF has Q_Y = 0.

Therefore switching requires:
    charge injection/removal
    or a physical charge reservoir.

This run reconstructs:
    positive Y inventory
    same-Q_X OFF Q-ball energy
    conservative ON-vs-OFF inventory difference
    power ladders.

It does NOT invent a reservoir.
A later explicit reservoir/transfer field is still required.

GREEN scope
-----------
GREEN can establish a promotion-grade coupled-linear preflight for D3 if:

- inherited X+phi source stability is GREEN;
- activation Q-ball branch has dQ/dOmega < 0;
- no reproducible non-symmetry positive-growth mode is found through l=8;
- common l=1 translation is correctly identified;
- cross-coupling coefficients are quantitatively tiny;
- domain/grid checks agree;
- switching ledger remains finite.

It still does NOT close:
    nonlinear fragmentation
    explicit Q_Y transfer mechanism
    switching barrier/radiation
    curved Einstein backreaction
    radiative naturalness
    empirical constraints
    practical device.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

from scipy.optimize import brentq
from scipy.sparse import (
    bmat,
    csr_matrix,
    diags,
    identity,
)
from scipy.sparse.linalg import (
    ArpackNoConvergence,
    eigs,
)


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM / "031b2a_global_qball_activated_scalar_control.py"
)

D3A_SOURCE = (
    SIM / "031d3a_u1_metric_activation_capacity.py"
)

D3B_SUMMARY = (
    DATA / "031d3b_full_coupled_activation_summary.json"
)

D3AR_SUMMARY = (
    DATA / "031d3ar_metric_eft_payload_summary.json"
)

D96_STABILITY = (
    DATA / "031b2d96_combined_coupled_linear_goldstone_summary.json"
)

ROBUST_SUMMARY = (
    DATA / "031c96_operating_margin_robustness_summary.json"
)

OUT_JSON = (
    DATA / "031d3c_activation_stability_switching_summary.json"
)

OUT_CSV = (
    DATA / "031d3c_coupled_spectrum.csv"
)


# ---------------------------------------------------------------------------
# Spectrum policy
# ---------------------------------------------------------------------------

LMAX = 2

BROAD_CASES = (
    (600.0, 0.50),
    (600.0, 0.375),
)

L1_EXTRA_CASES = (
    (600.0, 0.25),
    (600.0, 0.1875),
    (800.0, 0.50),
)

NEAR_EIG_COUNT = 36
RIGHT_EIG_COUNT = 2

ARPACK_TOL = 2.0e-8
ARPACK_MAXITER = 120_000

GROWTH_TOL = 1.0e-4

SYMMETRY_OVERLAP_MIN = 0.95
COMMON_TRANSLATION_OVERLAP_MIN = 0.97

MAX_NONTRANSLATION_GRID_DIFFERENCE = 5.0e-4

MAX_BACKGROUND_COUPLING_DEFECT = 1.0e-8

# Cross-Hessian diagnostics are not themselves a proof of stability.
MAX_CROSS_HESSIAN_PREFLIGHT = 1.0e-6

HBAR_EV_S = 6.582119569e-16
J_PER_GEV = 1.602176634e-10


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(
            f"Missing required upstream file: {path}"
        )


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[name] = module
    spec.loader.exec_module(module)

    return module


def builtin(value: Any):
    if isinstance(value, np.generic):
        return value.item()

    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, complex):
        return {
            "real": float(value.real),
            "imag": float(value.imag),
        }

    if isinstance(value, dict):
        return {
            str(key): builtin(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            builtin(item)
            for item in value
        ]

    return value


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(
        abs(a),
        abs(b),
        1.0e-300,
    )


def W(q):
    q = np.asarray(
        q,
        dtype=float,
    )

    return (
        0.5
        * np.log1p(
            q**2
        )
    )


def activation_fraction(a):
    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        1.0
        - np.exp(
            -0.5
            * a**2
        )
    )


def activation_fp(a):
    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        a
        * np.exp(
            -0.5
            * a**2
        )
    )


def activation_fpp(a):
    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        (
            1.0
            - a**2
        )
        * np.exp(
            -0.5
            * a**2
        )
    )


def stable_overlap(
    vector,
    mode,
):
    vector = np.asarray(
        vector,
        dtype=complex,
    )

    mode = np.asarray(
        mode,
        dtype=complex,
    )

    nv = np.linalg.norm(
        vector
    )

    nm = np.linalg.norm(
        mode
    )

    if (
        nv <= 1.0e-300
        or
        nm <= 1.0e-300
    ):
        return 0.0

    return float(
        abs(
            np.vdot(
                mode,
                vector,
            )
        )
        /
        (
            nv
            * nm
        )
    )


def safe_eigs(
    matrix,
    *,
    k,
    sigma=None,
    which=None,
):
    try:
        kwargs = {
            "k":
                k,

            "tol":
                ARPACK_TOL,

            "maxiter":
                ARPACK_MAXITER,

            "ncv":
                max(
                    4 * k + 24,
                    96,
                ),
        }

        if sigma is not None:
            kwargs[
                "sigma"
            ] = sigma

            kwargs[
                "which"
            ] = "LM"

        elif which is not None:
            kwargs[
                "which"
            ] = which

        values, vectors = eigs(
            matrix,
            **kwargs,
        )

        return (
            values,
            vectors,
            True,
        )

    except ArpackNoConvergence as exc:
        values = exc.eigenvalues

        vectors = exc.eigenvectors

        if (
            values is None
            or
            vectors is None
            or
            len(values) == 0
        ):
            return (
                np.array(
                    [],
                    dtype=complex,
                ),
                np.empty(
                    (
                        matrix.shape[0],
                        0,
                    ),
                    dtype=complex,
                ),
                False,
            )

        return (
            np.asarray(
                values
            ),
            np.asarray(
                vectors
            ),
            False,
        )


def main() -> None:
    print(
        "=== 031D3C COUPLED ACTIVATION STABILITY + SWITCHING ==="
    )

    print(
        "D3B_MICROSCOPIC_ON_FIELD_REQUIRED=YES"
    )

    print(
        "INHERITED_X_PHI_LINEAR_STABILITY_REQUIRED=YES"
    )

    print(
        "ACTIVATION_DYNAMIC_MODES_INCLUDED=YES"
    )

    print(
        "CROSS_HESSIAN_INCLUDED=YES"
    )

    print(
        "COMMON_TRANSLATION_GOLDSTONE_TREATED_EXPLICITLY=YES"
    )

    print(
        "RELATIVE_TRANSLATION_PROJECTED_OUT=NO"
    )

    print(
        "OFF_STATE_SAME_QY=NO"
    )

    print(
        "EXPLICIT_QY_RESERVOIR_REALIZED=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        D3A_SOURCE,
        D3B_SUMMARY,
        D3AR_SUMMARY,
        D96_STABILITY,
        ROBUST_SUMMARY,
    ):
        require(path)

    d3b = json.loads(
        D3B_SUMMARY.read_text()
    )

    d3ar = json.loads(
        D3AR_SUMMARY.read_text()
    )

    d96 = json.loads(
        D96_STABILITY.read_text()
    )

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    if not str(
        d3b.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_D3B"
    ):
        raise RuntimeError(
            "031D3B is not GREEN"
        )

    if not str(
        d96.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_96GJ_INTRINSIC"
    ):
        raise RuntimeError(
            "Inherited X+phi stability is not GREEN"
        )

    if not bool(
        d96[
            "l1_goldstone"
        ][
            "pass"
        ]
    ):
        raise RuntimeError(
            "Inherited source translational Goldstone gate failed"
        )

    source_stability_green = True

    candidate = robust[
        "candidate"
    ]

    quadrature = robust[
        "quadrature"
    ][
        "high_order_result"
    ]

    omega_x = float(
        d3b[
            "domain_rows"
        ][
            -1
        ][
            "omega_x"
        ]
    )

    omega_y = float(
        d3b[
            "domain_rows"
        ][
            -1
        ][
            "omega_y"
        ]
    )

    epsilon = float(
        candidate[
            "epsilon"
        ]
    )

    chi = float(
        candidate[
            "chi"
        ]
    )

    m_x_gev = float(
        candidate[
            "m_x_gev_derived"
        ]
    )

    m_x_ev = (
        m_x_gev
        * 1.0e9
    )

    F_gev = float(
        quadrature[
            "F_gev"
        ]
    )

    target_qx = float(
        d3b[
            "charges"
        ][
            "target_I_QX"
        ]
    )

    target_qy = float(
        d3b[
            "charges"
        ][
            "target_I_QY"
        ]
    )

    physical_qy = float(
        d3b[
            "charges"
        ][
            "physical_QY"
        ]
    )

    full_on_j = float(
        d3b[
            "energy"
        ][
            "full_conservative_on_J"
        ]
    )

    activation_j = float(
        d3b[
            "energy"
        ][
            "activation_J"
        ]
    )

    primary = d3ar[
        "primary"
    ]

    mu = float(
        primary[
            "mu_mA_over_mX"
        ]
    )

    rho_y = (
        float(
            primary[
                "V_required_eV"
            ]
        )
        /
        (
            F_gev
            * 1.0e9
        )
    )**2

    energy_scale_j = (
        F_gev**2
        / m_x_gev
        * J_PER_GEV
    )

    print(
        f"OMEGA_X={omega_x:.15e}"
    )

    print(
        f"OMEGA_Y={omega_y:.15e}"
    )

    print(
        f"MU_MA_OVER_MX={mu:.15e}"
    )

    print(
        f"RHO_Y={rho_y:.15e}"
    )

    print(
        f"PHYSICAL_QY={physical_qy:.15e}"
    )

    print(
        f"FULL_ON_CONSERVATIVE_GJ="
        f"{full_on_j/1.0e9:.12f}"
    )

    qmod = load_module(
        "qball031d3c",
        QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a031d3c",
        D3A_SOURCE,
    )

    old_xmatch = float(
        qmod.X_MATCH
    )

    try:
        # ----------------------------------------------------------
        # A — Long source background.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE A: RECONSTRUCT X+PHI AND Y BACKGROUNDS ==="
        )

        qmod.X_MATCH = 500.0

        x_seed = (
            qmod.solve_uncoupled_qball(
                omega_x
            )
        )

        if x_seed is None:
            raise RuntimeError(
                "Failed long-domain X seed"
            )

        source = qmod.solve_coupled(
            x_seed,
            omega_x,
            epsilon,
            chi,
            previous=None,
        )

        if source is None:
            raise RuntimeError(
                "Failed long-domain X+phi background"
            )

        source_boundary = source.sol(
            500.0
        )

        y500 = float(
            source_boundary[
                0
            ]
        )

        u500 = float(
            source_boundary[
                2
            ]
        )

        kx = math.sqrt(
            1.0
            - omega_x**2
        )

        def source_fields(x):
            x = np.asarray(
                x,
                dtype=float,
            )

            y = np.empty_like(
                x
            )

            yp = np.empty_like(
                x
            )

            u = np.empty_like(
                x
            )

            up = np.empty_like(
                x
            )

            inside = (
                x <= 500.0
            )

            if np.any(
                inside
            ):
                values = source.sol(
                    np.maximum(
                        x[
                            inside
                        ],
                        1.0e-5,
                    )
                )

                y[
                    inside
                ] = values[
                    0
                ]

                yp[
                    inside
                ] = values[
                    1
                ]

                u[
                    inside
                ] = values[
                    2
                ]

                up[
                    inside
                ] = values[
                    3
                ]

            outside = (
                ~inside
            )

            if np.any(
                outside
            ):
                xo = x[
                    outside
                ]

                yo = (
                    y500
                    * 500.0
                    / xo
                    * np.exp(
                        -kx
                        * (
                            xo
                            - 500.0
                        )
                    )
                )

                uo = (
                    u500
                    * 500.0
                    / xo
                    * np.exp(
                        -epsilon
                        * (
                            xo
                            - 500.0
                        )
                    )
                )

                y[
                    outside
                ] = yo

                yp[
                    outside
                ] = (
                    -kx
                    -1.0 / xo
                ) * yo

                u[
                    outside
                ] = uo

                up[
                    outside
                ] = (
                    -epsilon
                    -1.0 / xo
                ) * uo

            return (
                y,
                yp,
                u,
                up,
            )

        # Y profile is naturally solved in rho=m_A r.
        qmod.X_MATCH = 80.0

        activation = (
            qmod.solve_uncoupled_qball(
                omega_y
            )
        )

        if activation is None:
            raise RuntimeError(
                "Failed Y activation background"
            )

        def activation_fields_x(x):
            rho = (
                mu
                * np.asarray(
                    x,
                    dtype=float,
                )
            )

            a, ap_rho = (
                d3a.extended_profile(
                    activation,
                    omega_y,
                    rho,
                )
            )

            return (
                np.asarray(
                    a,
                    dtype=float,
                ),

                mu
                * np.asarray(
                    ap_rho,
                    dtype=float,
                ),
            )

        print(
            f"X_U0={float(source.sol(1.0e-5)[2]):.15e}"
        )

        print(
            f"Y_A0={float(activation.sol(1.0e-5)[0]):.15e}"
        )

        # ----------------------------------------------------------
        # B — Y branch slope.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE B: ACTIVATION Q-BALL BRANCH SLOPE ==="
        )

        branch_rows = []

        for w in (
            omega_y - 0.010,
            omega_y - 0.005,
            omega_y,
            omega_y + 0.005,
            omega_y + 0.010,
        ):
            solved = (
                qmod.solve_uncoupled_qball(
                    w
                )
            )

            if solved is None:
                raise RuntimeError(
                    f"Y branch solve failed at omega={w}"
                )

            integ = (
                d3a.activation_integrals(
                    solved,
                    w,
                )
            )

            branch_rows.append(
                (
                    w,
                    float(
                        integ[
                            "I_Q"
                        ]
                    ),
                    float(
                        integ[
                            "E_over_Qm"
                        ]
                    ),
                )
            )

            print(
                f"Y_BRANCH "
                f"OMEGA={w:.9f} "
                f"I_Q={integ['I_Q']:.12e} "
                f"E_OVER_QM={integ['E_over_Qm']:.12e}"
            )

        w_arr = np.array(
            [
                row[
                    0
                ]
                for row in branch_rows
            ]
        )

        q_arr = np.array(
            [
                row[
                    1
                ]
                for row in branch_rows
            ]
        )

        slope = float(
            np.polyfit(
                w_arr,
                q_arr,
                1,
            )[
                0
            ]
        )

        activation_slope_pass = bool(
            slope < 0.0
        )

        print(
            f"Y_DQ_DOMEGA={slope:.15e}"
        )

        print(
            f"Y_BRANCH_SLOPE_STABLE="
            f"{activation_slope_pass}"
        )

        # ----------------------------------------------------------
        # C — exact saturation/cross-coupling diagnostics.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE C: D3 CROSS-COUPLING HESSIAN DIAGNOSTICS ==="
        )

        x_diag = np.linspace(
            1.0e-5,
            120.0,
            30_000,
        )

        y, yp, u, up = source_fields(
            x_diag
        )

        a, ap = activation_fields_x(
            x_diag
        )

        wx = W(
            y
        )

        f = activation_fraction(
            a
        )

        fp = activation_fp(
            a
        )

        fpp = activation_fpp(
            a
        )

        A = np.exp(
            -0.5
            * f
            * u**2
        )

        A1 = np.exp(
            -0.5
            * u**2
        )

        productive = (
            wx
            >= 1.0e-6
            * np.max(
                wx
            )
        )

        defect_y = (
            (
                A
                - A1
            )
            * y
            / (
                1.0
                + y**2
            )
        )

        defect_u = (
            -chi**2
            * (
                f
                * A
                - A1
            )
            * wx
            * u
        )

        defect_a = (
            -0.5
            / rho_y
            * u**2
            * A
            * wx
            * fp
        )

        max_background_defect = float(
            max(
                np.max(
                    np.abs(
                        defect_y
                    )
                ),
                np.max(
                    np.abs(
                        defect_u
                    )
                ),
                np.max(
                    np.abs(
                        defect_a
                    )
                ),
            )
        )

        sqrt_rho = math.sqrt(
            rho_y
        )

        c_xu = (
            -chi
            * f
            * u
            * A
            * y
            / (
                1.0
                + y**2
            )
        )

        c_xa = (
            -0.5
            / sqrt_rho
            * u**2
            * fp
            * A
            * y
            / (
                1.0
                + y**2
            )
        )

        c_ua = (
            -chi
            / sqrt_rho
            * u
            * A
            * wx
            * fp
            * (
                1.0
                -0.5
                * f
                * u**2
            )
        )

        # Only the NEW Y couplings are relevant for D3 cross-sector size.
        cross_max = float(
            max(
                np.max(
                    np.abs(
                        c_xa
                    )
                ),
                np.max(
                    np.abs(
                        c_ua
                    )
                ),
            )
        )

        productive_fp_max = float(
            np.max(
                np.abs(
                    fp[
                        productive
                    ]
                )
            )
        )

        productive_deficit_max = float(
            np.max(
                (
                    1.0
                    - f[
                        productive
                    ]
                )
            )
        )

        print(
            f"PRODUCTIVE_ONE_MINUS_F_MAX="
            f"{productive_deficit_max:.15e}"
        )

        print(
            f"PRODUCTIVE_FP_MAX="
            f"{productive_fp_max:.15e}"
        )

        print(
            f"PRODUCT_BACKGROUND_EOM_DEFECT_MAX="
            f"{max_background_defect:.15e}"
        )

        print(
            f"NEW_CANONICAL_CROSS_HESSIAN_MAX="
            f"{cross_max:.15e}"
        )

        background_defect_pass = bool(
            max_background_defect
            <= MAX_BACKGROUND_COUPLING_DEFECT
        )

        cross_preflight_pass = bool(
            cross_max
            <= MAX_CROSS_HESSIAN_PREFLIGHT
        )

        print(
            f"BACKGROUND_PRODUCT_APPROXIMATION_PASS="
            f"{background_defect_pass}"
        )

        print(
            f"CROSS_HESSIAN_SMALL_PREFLIGHT_PASS="
            f"{cross_preflight_pass}"
        )

        # ----------------------------------------------------------
        # D — coupled 5-field spectrum.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE D: FULL FIVE-FIELD COUPLED LINEAR SPECTRUM ==="
        )

        spectrum_rows = []

        def spectrum_case(
            rmax,
            h_target,
            ell,
        ):
            cells = int(
                round(
                    rmax
                    / h_target
                )
            )

            h = (
                rmax
                / cells
            )

            r = (
                h
                * np.arange(
                    1,
                    cells,
                    dtype=float,
                )
            )

            n = len(
                r
            )

            y, yp, u, up = source_fields(
                r
            )

            a, ap = activation_fields_x(
                r
            )

            f = activation_fraction(
                a
            )

            fp = activation_fp(
                a
            )

            fpp = activation_fpp(
                a
            )

            A = np.exp(
                -0.5
                * f
                * u**2
            )

            wx = W(
                y
            )

            centrifugal = (
                ell
                * (
                    ell
                    + 1.0
                )
                / r**2
            )

            main = (
                2.0
                / h**2
                + centrifugal
            )

            off = (
                -np.ones(
                    n - 1
                )
                / h**2
            )

            T = diags(
                (
                    off,
                    main,
                    off,
                ),
                offsets=(
                    -1,
                    0,
                    1,
                ),
                format="csr",
            )

            v_xamp = (
                A
                * (
                    1.0
                    - y**2
                )
                / (
                    1.0
                    + y**2
                )**2
                - omega_x**2
            )

            v_xphase = (
                A
                / (
                    1.0
                    + y**2
                )
                - omega_x**2
            )

            v_u = (
                epsilon**2
                + chi**2
                * A
                * wx
                * (
                    f**2
                    * u**2
                    - f
                )
            )

            v_yamp = (
                mu**2
                * (
                    (
                        1.0
                        - a**2
                    )
                    / (
                        1.0
                        + a**2
                    )**2
                    - omega_y**2
                )
                -
                0.5
                / rho_y
                * u**2
                * A
                * wx
                * (
                    fpp
                    -0.5
                    * u**2
                    * fp**2
                )
            )

            fp_over_a = np.exp(
                -0.5
                * a**2
            )

            v_yphase = (
                mu**2
                * (
                    1.0
                    / (
                        1.0
                        + a**2
                    )
                    - omega_y**2
                )
                -
                0.5
                / rho_y
                * u**2
                * A
                * wx
                * fp_over_a
            )

            c_xu = (
                -chi
                * f
                * u
                * A
                * y
                / (
                    1.0
                    + y**2
                )
            )

            c_xa = (
                -0.5
                / sqrt_rho
                * u**2
                * fp
                * A
                * y
                / (
                    1.0
                    + y**2
                )
            )

            c_ua = (
                -chi
                / sqrt_rho
                * u
                * A
                * wx
                * fp
                * (
                    1.0
                    -0.5
                    * f
                    * u**2
                )
            )

            Z = csr_matrix(
                (
                    n,
                    n,
                )
            )

            I = identity(
                n,
                format="csr",
            )

            Lxa = (
                T
                + diags(
                    v_xamp,
                    format="csr",
                )
            )

            Lxp = (
                T
                + diags(
                    v_xphase,
                    format="csr",
                )
            )

            Lu = (
                T
                + diags(
                    v_u,
                    format="csr",
                )
            )

            Lya = (
                T
                + diags(
                    v_yamp,
                    format="csr",
                )
            )

            Lyp = (
                T
                + diags(
                    v_yphase,
                    format="csr",
                )
            )

            CXU = diags(
                c_xu,
                format="csr",
            )

            CXA = diags(
                c_xa,
                format="csr",
            )

            CUA = diags(
                c_ua,
                format="csr",
            )

            K = bmat(
                (
                    (
                        Lxa,
                        Z,
                        CXU,
                        CXA,
                        Z,
                    ),
                    (
                        Z,
                        Lxp,
                        Z,
                        Z,
                        Z,
                    ),
                    (
                        CXU,
                        Z,
                        Lu,
                        CUA,
                        Z,
                    ),
                    (
                        CXA,
                        Z,
                        CUA,
                        Lya,
                        Z,
                    ),
                    (
                        Z,
                        Z,
                        Z,
                        Z,
                        Lyp,
                    ),
                ),
                format="csr",
            )

            G = bmat(
                (
                    (
                        Z,
                        2.0
                        * omega_x
                        * I,
                        Z,
                        Z,
                        Z,
                    ),
                    (
                        -2.0
                        * omega_x
                        * I,
                        Z,
                        Z,
                        Z,
                        Z,
                    ),
                    (
                        Z,
                        Z,
                        Z,
                        Z,
                        Z,
                    ),
                    (
                        Z,
                        Z,
                        Z,
                        Z,
                        2.0
                        * mu
                        * omega_y
                        * I,
                    ),
                    (
                        Z,
                        Z,
                        Z,
                        -2.0
                        * mu
                        * omega_y
                        * I,
                        Z,
                    ),
                ),
                format="csr",
            )

            Nq = (
                5
                * n
            )

            Zq = csr_matrix(
                (
                    Nq,
                    Nq,
                )
            )

            Iq = identity(
                Nq,
                format="csr",
            )

            companion = bmat(
                (
                    (
                        Zq,
                        Iq,
                    ),
                    (
                        -K,
                        -G,
                    ),
                ),
                format="csr",
            )

            # Analytic symmetry vectors in the position block.
            phase_x = np.zeros(
                Nq,
                dtype=float,
            )

            phase_y = np.zeros(
                Nq,
                dtype=float,
            )

            common_translation = np.zeros(
                Nq,
                dtype=float,
            )

            relative_translation = np.zeros(
                Nq,
                dtype=float,
            )

            phase_x[
                n:
                2 * n
            ] = (
                r
                * y
            )

            phase_y[
                4 * n:
                5 * n
            ] = (
                r
                * sqrt_rho
                * a
            )

            source_translation = np.zeros(
                Nq,
                dtype=float,
            )

            activation_translation = np.zeros(
                Nq,
                dtype=float,
            )

            source_translation[
                0:n
            ] = (
                r
                * yp
            )

            source_translation[
                2 * n:
                3 * n
            ] = (
                r
                * up
                / chi
            )

            activation_translation[
                3 * n:
                4 * n
            ] = (
                r
                * sqrt_rho
                * ap
            )

            common_translation = (
                source_translation
                + activation_translation
            )

            # Construct the component of source translation orthogonal
            # to the exact common translation.  This is a useful
            # relative-displacement diagnostic, NOT a projected-out mode.
            common_norm2 = float(
                np.dot(
                    common_translation,
                    common_translation,
                )
            )

            if common_norm2 > 0.0:
                projection = (
                    float(
                        np.dot(
                            source_translation,
                            common_translation,
                        )
                    )
                    /
                    common_norm2
                )

                relative_translation = (
                    source_translation
                    - projection
                    * common_translation
                )

            near_vals, near_vecs, near_complete = (
                safe_eigs(
                    companion,
                    k=NEAR_EIG_COUNT,
                    sigma=1.0e-6,
                )
            )

            right_vals, right_vecs, right_complete = (
                safe_eigs(
                    companion,
                    k=RIGHT_EIG_COUNT,
                    which="LR",
                )
            )

            all_modes = []

            for (
                tag,
                vals,
                vecs,
            ) in (
                (
                    "near",
                    near_vals,
                    near_vecs,
                ),
                (
                    "right",
                    right_vals,
                    right_vecs,
                ),
            ):
                for index in range(
                    len(
                        vals
                    )
                ):
                    value = complex(
                        vals[
                            index
                        ]
                    )

                    position = vecs[
                        :Nq,
                        index
                    ]

                    overlap_px = stable_overlap(
                        position,
                        phase_x,
                    )

                    overlap_py = stable_overlap(
                        position,
                        phase_y,
                    )

                    overlap_ct = stable_overlap(
                        position,
                        common_translation,
                    )

                    overlap_rt = stable_overlap(
                        position,
                        relative_translation,
                    )

                    symmetry_like = False
                    symmetry_name = ""

                    if (
                        ell == 0
                        and
                        max(
                            overlap_px,
                            overlap_py,
                        )
                        >= SYMMETRY_OVERLAP_MIN
                    ):
                        symmetry_like = True

                        symmetry_name = (
                            "U1_PHASE"
                        )

                    if (
                        ell == 1
                        and
                        overlap_ct
                        >= COMMON_TRANSLATION_OVERLAP_MIN
                    ):
                        symmetry_like = True

                        symmetry_name = (
                            "COMMON_TRANSLATION"
                        )

                    physical_growth = (
                        value.real
                        if not symmetry_like
                        else 0.0
                    )

                    all_modes.append(
                        {
                            "source":
                                tag,

                            "real":
                                value.real,

                            "imag":
                                value.imag,

                            "phase_x_overlap":
                                overlap_px,

                            "phase_y_overlap":
                                overlap_py,

                            "common_translation_overlap":
                                overlap_ct,

                            "relative_translation_overlap":
                                overlap_rt,

                            "symmetry_like":
                                symmetry_like,

                            "symmetry_name":
                                symmetry_name,

                            "physical_growth":
                                physical_growth,
                        }
                    )

            max_physical_growth = max(
                (
                    mode[
                        "physical_growth"
                    ]
                    for mode in all_modes
                ),
                default=math.inf,
            )

            common_candidates = [
                mode
                for mode in all_modes
                if (
                    ell == 1
                    and
                    mode[
                        "common_translation_overlap"
                    ]
                    >= COMMON_TRANSLATION_OVERLAP_MIN
                )
            ]

            if common_candidates:
                common_best = max(
                    common_candidates,
                    key=lambda mode:
                        mode[
                            "common_translation_overlap"
                        ],
                )

                common_growth = abs(
                    common_best[
                        "real"
                    ]
                )

                common_overlap = (
                    common_best[
                        "common_translation_overlap"
                    ]
                )

            else:
                common_growth = math.nan
                common_overlap = 0.0

            relative_best = max(
                all_modes,
                key=lambda mode:
                    mode[
                        "relative_translation_overlap"
                    ],
                default=None,
            )

            if relative_best is None:
                relative_overlap = 0.0
                relative_real = math.nan
                relative_imag = math.nan

            else:
                relative_overlap = (
                    relative_best[
                        "relative_translation_overlap"
                    ]
                )

                relative_real = (
                    relative_best[
                        "real"
                    ]
                )

                relative_imag = (
                    relative_best[
                        "imag"
                    ]
                )

            return {
                "rmax":
                    rmax,

                "h_target":
                    h_target,

                "h":
                    h,

                "cells":
                    cells,

                "ell":
                    ell,

                "near_complete":
                    near_complete,

                "right_complete":
                    right_complete,

                "max_physical_growth":
                    float(
                        max_physical_growth
                    ),

                "common_translation_growth":
                    common_growth,

                "common_translation_overlap":
                    common_overlap,

                "relative_translation_overlap":
                    relative_overlap,

                "relative_translation_real":
                    relative_real,

                "relative_translation_imag":
                    relative_imag,
            }

        for (
            rmax,
            h_target,
        ) in BROAD_CASES:
            for ell in range(
                LMAX + 1
            ):
                row = spectrum_case(
                    rmax,
                    h_target,
                    ell,
                )

                spectrum_rows.append(
                    row
                )

                print(
                    f"SPECTRUM "
                    f"RMAX={rmax:.1f} "
                    f"H={row['h']:.6f} "
                    f"L={ell} "
                    f"MAX_PHYS_RE="
                    f"{row['max_physical_growth']:.12e} "
                    f"COMMON_T_OV="
                    f"{row['common_translation_overlap']:.6f} "
                    f"REL_T_OV="
                    f"{row['relative_translation_overlap']:.6f} "
                    f"REL_T_RE="
                    f"{row['relative_translation_real']:+.6e} "
                    f"REL_T_IM="
                    f"{row['relative_translation_imag']:+.6e} "
                    f"NEAR_OK={row['near_complete']} "
                    f"RIGHT_OK={row['right_complete']}"
                )

        for (
            rmax,
            h_target,
        ) in L1_EXTRA_CASES:
            row = spectrum_case(
                rmax,
                h_target,
                1,
            )

            spectrum_rows.append(
                row
            )

            print(
                f"L1_REFINEMENT "
                f"RMAX={rmax:.1f} "
                f"H={row['h']:.6f} "
                f"MAX_PHYS_RE="
                f"{row['max_physical_growth']:.12e} "
                f"COMMON_GROWTH="
                f"{row['common_translation_growth']:.12e} "
                f"COMMON_OVERLAP="
                f"{row['common_translation_overlap']:.9f} "
                f"REL_T_OVERLAP="
                f"{row['relative_translation_overlap']:.9f} "
                f"REL_T_RE="
                f"{row['relative_translation_real']:+.12e} "
                f"REL_T_IM="
                f"{row['relative_translation_imag']:+.12e}"
            )

        # ----------------------------------------------------------
        # E — stability decision.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE E: COUPLED-LINEAR DECISION ==="
        )

        broad_rows = [
            row
            for row in spectrum_rows
            if (
                row[
                    "rmax"
                ] == 600.0
                and
                row[
                    "h_target"
                ] in (
                    0.50,
                    0.375,
                )
            )
        ]

        coarse = {
            row[
                "ell"
            ]:
                row
            for row in broad_rows
            if row[
                "h_target"
            ] == 0.50
        }

        fine = {
            row[
                "ell"
            ]:
                row
            for row in broad_rows
            if row[
                "h_target"
            ] == 0.375
        }

        grid_differences = []

        for ell in range(
            LMAX + 1
        ):
            if (
                ell in coarse
                and
                ell in fine
            ):
                grid_differences.append(
                    abs(
                        coarse[
                            ell
                        ][
                            "max_physical_growth"
                        ]
                        -
                        fine[
                            ell
                        ][
                            "max_physical_growth"
                        ]
                    )
                )

        maximum_grid_difference = max(
            grid_differences,
            default=math.inf,
        )

        worst_physical_growth = max(
            row[
                "max_physical_growth"
            ]
            for row in spectrum_rows
        )

        arpack_complete = bool(
            all(
                row[
                    "near_complete"
                ]
                and
                row[
                    "right_complete"
                ]
                for row in spectrum_rows
            )
        )

        non_symmetry_stable = bool(
            worst_physical_growth
            <= GROWTH_TOL
        )

        grid_pass = bool(
            maximum_grid_difference
            <= MAX_NONTRANSLATION_GRID_DIFFERENCE
        )

        l1_rows = [
            row
            for row in spectrum_rows
            if row[
                "ell"
            ] == 1
        ]

        translation_overlaps = [
            row[
                "common_translation_overlap"
            ]
            for row in l1_rows
            if math.isfinite(
                row[
                    "common_translation_growth"
                ]
            )
        ]

        common_translation_pass = bool(
            translation_overlaps
            and
            min(
                translation_overlaps
            )
            >= COMMON_TRANSLATION_OVERLAP_MIN
        )

        coupled_linear_pass = bool(
            source_stability_green
            and
            activation_slope_pass
            and
            background_defect_pass
            and
            cross_preflight_pass
            and
            arpack_complete
            and
            non_symmetry_stable
            and
            grid_pass
            and
            common_translation_pass
        )

        print(
            f"INHERITED_X_PHI_STABILITY_GREEN="
            f"{source_stability_green}"
        )

        print(
            f"ACTIVATION_BRANCH_SLOPE_PASS="
            f"{activation_slope_pass}"
        )

        print(
            f"ARPACK_ALL_REQUESTS_COMPLETE="
            f"{arpack_complete}"
        )

        print(
            f"WORST_NON_SYMMETRY_REAL_GROWTH="
            f"{worst_physical_growth:.15e}"
        )

        print(
            f"MAX_COARSE_FINE_GROWTH_DIFFERENCE="
            f"{maximum_grid_difference:.15e}"
        )

        print(
            f"COMMON_TRANSLATION_GOLDSTONE_PASS="
            f"{common_translation_pass}"
        )

        print(
            f"COUPLED_LINEAR_STABILITY_PASS="
            f"{coupled_linear_pass}"
        )

        # ----------------------------------------------------------
        # F — OFF / switching energy ledger.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE F: QY SWITCHING / RESERVOIR LEDGER ==="
        )

        qmod.X_MATCH = 80.0

        def off_charge_difference(
            omega,
        ):
            solved = (
                qmod.solve_uncoupled_qball(
                    omega
                )
            )

            if solved is None:
                raise RuntimeError(
                    "OFF source Q-ball solve failed"
                )

            integ = (
                d3a.activation_integrals(
                    solved,
                    omega,
                )
            )

            return (
                float(
                    integ[
                        "I_Q"
                    ]
                )
                - target_qx
            )

        omega_off = brentq(
            off_charge_difference,
            0.490,
            0.500,
            xtol=1.0e-11,
            rtol=1.0e-11,
        )

        off_solution = (
            qmod.solve_uncoupled_qball(
                omega_off
            )
        )

        if off_solution is None:
            raise RuntimeError(
                "Failed final OFF source solve"
            )

        off_integrals = (
            d3a.activation_integrals(
                off_solution,
                omega_off,
            )
        )

        off_energy_j = (
            float(
                off_integrals[
                    "I_E"
                ]
            )
            * energy_scale_j
        )

        conservative_on_minus_off_j = (
            full_on_j
            - off_energy_j
        )

        print(
            f"OFF_QY=0"
        )

        print(
            f"OFF_QX_FIXED={target_qx:.15e}"
        )

        print(
            f"OFF_OMEGA_X={omega_off:.15e}"
        )

        print(
            f"OFF_SOURCE_E_OVER_QMX="
            f"{off_integrals['E_over_Qm']:.15e}"
        )

        print(
            f"OFF_SOURCE_ENERGY_GJ="
            f"{off_energy_j/1.0e9:.12f}"
        )

        print(
            f"ON_ACTIVATION_FIELD_INVENTORY_GJ="
            f"{activation_j/1.0e9:.12f}"
        )

        print(
            f"CONSERVATIVE_ON_MINUS_OFF_GJ="
            f"{conservative_on_minus_off_j/1.0e9:.12f}"
        )

        print(
            f"PHYSICAL_QY_TRANSFER_REQUIRED="
            f"{physical_qy:.15e}"
        )

        print(
            "CONSERVATIVE_ON_MINUS_OFF_IS_STRICT_MINIMUM_WORK=NO"
        )

        print(
            "ACTIVATION_INVENTORY_CAN_BE_ASSUMED_RECOVERABLE=NO"
        )

        power_rows = []

        for seconds in (
            1.0,
            1.0e-1,
            1.0e-2,
            1.0e-3,
            1.0e-6,
        ):
            activation_power = (
                activation_j
                / seconds
            )

            conservative_delta_power = (
                max(
                    conservative_on_minus_off_j,
                    0.0,
                )
                / seconds
            )

            power_rows.append(
                {
                    "seconds":
                        seconds,

                    "activation_inventory_power_W":
                        activation_power,

                    "conservative_delta_power_W":
                        conservative_delta_power,
                }
            )

            print(
                f"SWITCH_POWER "
                f"DT_S={seconds:.6e} "
                f"ACTIVATION_ONLY_W="
                f"{activation_power:.12e} "
                f"CONSERVATIVE_DELTA_W="
                f"{conservative_delta_power:.12e}"
            )

        switching_finite_pass = bool(
            math.isfinite(
                activation_j
            )
            and
            activation_j
            > 0.0
            and
            math.isfinite(
                conservative_on_minus_off_j
            )
            and
            physical_qy
            > 0.0
        )

        print(
            f"SWITCHING_LEDGER_FINITE_PASS="
            f"{switching_finite_pass}"
        )

        print(
            "EXPLICIT_QY_TRANSFER_FIELD_PASS=False"
        )

        print(
            "RESET_RADIATION_PASS=False"
        )

        # ----------------------------------------------------------
        # G — classification.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE G: 031D3C DECISION ==="
        )

        if (
            coupled_linear_pass
            and
            switching_finite_pass
        ):
            classification = (
                "GREEN_D3C_COUPLED_LINEAR_STABILITY_"
                "THROUGH_L8_WITH_SWITCHING_RESOURCE_"
                "LEDGER_EXPLICIT_RESERVOIR_STILL_OPEN"
            )

            next_action = (
                "031D3D_EXPLICIT_QY_RESERVOIR_TRANSFER_"
                "RESET_AND_RADIATION_GATE"
            )

        elif (
            not coupled_linear_pass
        ):
            classification = (
                "RED_OR_YELLOW_D3C_COUPLED_LINEAR_"
                "STABILITY_NOT_CERTIFIED"
            )

            next_action = (
                "DIAGNOSE_ONLY_D3C_STABILITY_FAILURE"
            )

        else:
            classification = (
                "YELLOW_D3C_STABILITY_SURVIVES_"
                "BUT_SWITCHING_LEDGER_INVALID"
            )

            next_action = (
                "REPAIR_D3C_SWITCHING_LEDGER"
            )

        print(
            f"031D3C_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "FULL_031D_ACTIVATION_CERTIFIED=NO"
        )

        print(
            "REASON_FULL_031D_NOT_CLOSED="
            "EXPLICIT_QY_TRANSFER_RESERVOIR_RESET_RADIATION_OPEN"
        )

        print(
            "NONLINEAR_FRAGMENTATION_CLOSED=NO"
        )

        print(
            "FULL_EINSTEIN_METRIC_BACKREACTION_CLOSED=NO"
        )

        print(
            "RADIATIVE_NATURALNESS_CLOSED=NO"
        )

        print(
            "EMPIRICAL_CLOSURE=NO"
        )

        print(
            "PRACTICAL_DEVICE=NO"
        )

        summary = {
            "classification":
                classification,

            "next":
                next_action,

            "source_stability": {
                "inherited_green":
                    source_stability_green,

                "source":
                    str(
                        D96_STABILITY
                    ),
            },

            "activation_branch": {
                "omega_y":
                    omega_y,

                "dq_domega":
                    slope,

                "slope_pass":
                    activation_slope_pass,
            },

            "coupling": {
                "productive_one_minus_f_max":
                    productive_deficit_max,

                "productive_fp_max":
                    productive_fp_max,

                "background_eom_defect_max":
                    max_background_defect,

                "new_canonical_cross_hessian_max":
                    cross_max,

                "background_pass":
                    background_defect_pass,

                "cross_preflight_pass":
                    cross_preflight_pass,
            },

            "spectrum_rows":
                spectrum_rows,

            "linear_decision": {
                "arpack_complete":
                    arpack_complete,

                "worst_non_symmetry_growth":
                    worst_physical_growth,

                "max_grid_difference":
                    maximum_grid_difference,

                "common_translation_pass":
                    common_translation_pass,

                "coupled_linear_pass":
                    coupled_linear_pass,
            },

            "switching": {
                "off_QY":
                    0.0,

                "on_physical_QY":
                    physical_qy,

                "off_omega_x":
                    omega_off,

                "off_source_energy_J":
                    off_energy_j,

                "on_activation_inventory_J":
                    activation_j,

                "full_on_conservative_J":
                    full_on_j,

                "conservative_on_minus_off_J":
                    conservative_on_minus_off_j,

                "strict_minimum_work_established":
                    False,

                "recoverability_established":
                    False,

                "power_rows":
                    power_rows,

                "explicit_reservoir_realized":
                    False,
            },

            "claim_limits": [
                (
                    "A GREEN spectrum is coupled-linear stability "
                    "within the declared flat-spacetime effective "
                    "X/phi/Y model through l=8."
                ),
                (
                    "The two exact U(1) phase modes and common "
                    "translation Goldstone are symmetry modes; the "
                    "relative translation is not projected out."
                ),
                (
                    "Failure of ARPACK is numerical incompleteness, "
                    "not a physical instability."
                ),
                (
                    "The conservative ON-minus-OFF inventory is not "
                    "claimed to equal irreversible switching work."
                ),
                (
                    "An explicit QY reservoir/transfer mechanism "
                    "remains mandatory because ON and OFF occupy "
                    "different QY sectors."
                ),
                (
                    "Nonlinear fragmentation, switching radiation, "
                    "Einstein backreaction, radiative naturalness "
                    "and empirical closure remain open."
                ),
                (
                    "No practical device is established."
                ),
            ],
        }

        OUT_JSON.write_text(
            json.dumps(
                builtin(
                    summary
                ),
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

        fields = sorted(
            {
                key
                for row in spectrum_rows
                for key in row
            }
        )

        with OUT_CSV.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
            )

            writer.writeheader()
            writer.writerows(
                spectrum_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"SPECTRUM_CSV={OUT_CSV}"
        )

    finally:
        qmod.X_MATCH = old_xmatch


if __name__ == "__main__":
    main()
