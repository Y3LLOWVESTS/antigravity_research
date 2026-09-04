"""
031D3A-R
========

EFT / self-coupling / finite-payload reaction repair for the independent
global-U(1) metric-activation mechanism.

D3A established a strong capacity result, but its minimum-energy point sat
exactly at

    m_A^2 / V^2 = 4 pi

and therefore minimized the activation inventory by saturating a permissive
strong-coupling boundary.

This run does NOT yet solve the fully coupled X + phi + Y fields.

Instead it asks whether the D3 mechanism remains attractive after:

    1. requiring an interior weak activation self-coupling;
    2. imposing explicit metric-operator cutoff sensitivity;
    3. calculating finite ordinary-payload backreaction on Y;
    4. checking that grad f(a) does not materially distort the physical
       metric force across the payload;
    5. counting the resulting physical activation charge and joules.

Physical metric
---------------

    log A = -1/2 f(a) u^2

    f(a) = 1 - exp(-a^2/2).

For canonical activation amplitude sigma = V a, ordinary matter sources the
activation equation through

    |delta L_m / delta sigma|
      <= |T| |u|^2 |f'(a)| / (2 V).

Compare this with the local intrinsic activation-Q-ball force scale

    m_A^2 V [
        |a|/(1+a^2)
        + Omega_A^2 |a|
    ].

The conservative dimensionless reaction estimate is therefore

    R_payload
      =
    |T| u^2 |f'(a)|
    /
    [
        2 m_A^2 V^2
        (
            |a|/(1+a^2)
            + Omega_A^2 |a|
        )
    ].

We deliberately use the magnitude of the payload rest-energy trace, without
credit from conformal suppression, making this a conservative preflight.

Metric-force contamination
--------------------------

    d_x log A
      =
    - f u u'
    - 1/2 u^2 f_x.

Compare directly with the inherited saturated result

    d_x log A_baseline = -u u'.

Promotion requires the whole sampled finite payload to remain close.

Metric EFT sensitivity
----------------------

The leading OFF-vacuum metric operator has schematic scale

    Lambda_metric ~ sqrt(V M_c).

Report sensitivity at

    1 MeV
    1 GeV
    10 GeV   <-- declared pre-D3B robustness floor
    100 GeV  <-- stress diagnostic, not promotion requirement.

A 10-GeV GREEN is NOT full EFT/naturalness closure.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM / "031b2a_global_qball_activated_scalar_control.py"
)

D3A_SOURCE = (
    SIM / "031d3a_u1_metric_activation_capacity.py"
)

ROBUST_SUMMARY = (
    DATA / "031c96_operating_margin_robustness_summary.json"
)

D3A_SUMMARY = (
    DATA / "031d3a_u1_metric_activation_summary.json"
)

D3A_SCAN = (
    DATA / "031d3a_u1_metric_activation_scan.csv"
)

OUT_JSON = (
    DATA / "031d3ar_metric_eft_payload_summary.json"
)

OUT_CSV = (
    DATA / "031d3ar_metric_eft_payload_scan.csv"
)


# ---------------------------------------------------------------------------
# Declared robustness gates
# ---------------------------------------------------------------------------

METRIC_CUTOFFS_EV = (
    1.0e6,
    1.0e9,
    1.0e10,
    1.0e11,
)

PRIMARY_METRIC_CUTOFF_EV = 1.0e10

# Move well inside the D3A 4*pi boundary.
MAX_ACTIVATION_SELF_COUPLING = 0.10

MAX_SOURCE_REACTION_RATIO = 0.10
MAX_PAYLOAD_REACTION_RATIO = 0.10

MIN_ACTIVATION_F = 0.999

MAX_METRIC_GRADIENT_RELERR = 5.0e-3

MAX_PRIMARY_ACTIVATION_ENERGY_FRACTION = 0.10

MIN_CLASSICAL_ACTIVATION_CHARGE = 1.0e6

# Declared finite payload used for backreaction.
PAYLOAD_MASS_KG = 1.0

# Sampling.
PAYLOAD_RADIAL_ORDER = 18
PAYLOAD_ANGULAR_ORDER = 28
PAYLOAD_SURFACE_POINTS = 181

X_MATCH = 80.0

C_LIGHT = 299_792_458.0
HBARC_EV_M = 1.973269804e-7
J_PER_EV = 1.602176634e-19


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(
            f"Missing required file: {path}"
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


def builtin(value):
    if isinstance(value, np.generic):
        return value.item()

    if isinstance(value, np.ndarray):
        return value.tolist()

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


def truth(value) -> bool:
    if isinstance(value, bool):
        return value

    return str(
        value
    ).strip().lower() in (
        "true",
        "1",
        "yes",
    )


def read_scan():
    rows = []

    with D3A_SCAN.open(
        newline="",
    ) as handle:
        reader = csv.DictReader(
            handle
        )

        for raw in reader:
            row = {}

            for key, value in raw.items():
                if key.endswith(
                    "_pass"
                ):
                    row[key] = truth(
                        value
                    )

                else:
                    try:
                        row[key] = float(
                            value
                        )
                    except (
                        TypeError,
                        ValueError,
                    ):
                        row[key] = value

            rows.append(
                row
            )

    return rows


def main() -> None:
    print(
        "=== 031D3A-R METRIC EFT + FINITE-PAYLOAD REACTION GATE ==="
    )

    print(
        "D3A_GEOMETRIC_CAPACITY_INHERITED=YES"
    )

    print(
        "D3A_TINY_7E_MINUS23J_QUOTE_PROMOTED=NO"
    )

    print(
        "REASON="
        "D3A_OPTIMUM_SATURATED_4PI_SELF_COUPLING_BOUNDARY"
    )

    print(
        "FULL_X_PHI_Y_COUPLED_FIELD_SOLVE=NO"
    )

    print(
        "PRIMARY_METRIC_CUTOFF_GEV="
        f"{PRIMARY_METRIC_CUTOFF_EV / 1.0e9:.6f}"
    )

    print(
        "PRIMARY_CUTOFF_IS_FINAL_UV_COMPLETION=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        D3A_SOURCE,
        ROBUST_SUMMARY,
        D3A_SUMMARY,
        D3A_SCAN,
    ):
        require(path)

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    d3_summary = json.loads(
        D3A_SUMMARY.read_text()
    )

    if not str(
        d3_summary.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_D3A"
    ):
        raise RuntimeError(
            "031D3A is not GREEN"
        )

    rows = read_scan()

    inherited = [
        row
        for row in rows
        if bool(
            row.get(
                "candidate_pass",
                False,
            )
        )
    ]

    if not inherited:
        raise RuntimeError(
            "No inherited D3A passing candidates"
        )

    candidate = robust[
        "candidate"
    ]

    operating = robust[
        "interior_20pct_margin_point"
    ]

    quadrature = robust[
        "quadrature"
    ][
        "high_order_result"
    ]

    nominal_geometry = next(
        row
        for row in robust[
            "geometry_scan"
        ]
        if row[
            "label"
        ] == "nominal"
    )

    omega_source = float(
        candidate[
            "omega"
        ]
    )

    epsilon = float(
        candidate[
            "epsilon"
        ]
    )

    chi_source = float(
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

    F_ev = (
        F_gev
        * 1.0e9
    )

    M_c_gev = (
        F_gev
        / chi_source
    )

    M_c_ev = (
        M_c_gev
        * 1.0e9
    )

    operating_energy_j = float(
        operating[
            "energy_J"
        ]
    )

    source_shift_m = float(
        operating[
            "shift_m"
        ]
    )

    payload_center_m = float(
        nominal_geometry[
            "payload_center_m"
        ]
    )

    payload_radius_m = float(
        nominal_geometry[
            "payload_radius_m"
        ]
    )

    payload_center_from_source_m = abs(
        payload_center_m
        - source_shift_m
    )

    payload_volume_m3 = (
        4.0
        * math.pi
        * payload_radius_m**3
        / 3.0
    )

    payload_density_kg_m3 = (
        PAYLOAD_MASS_KG
        / payload_volume_m3
    )

    payload_trace_j_m3 = (
        payload_density_kg_m3
        * C_LIGHT**2
    )

    # Natural-units energy density:
    #
    # 1 J = 1/J_PER_EV eV
    # 1 m^3 = (1/HBARC)^3 eV^-3.
    #
    # Hence rho[eV^4] =
    # rho[J/m^3] / J_PER_EV * HBARC^3.
    payload_trace_ev4 = (
        payload_trace_j_m3
        / J_PER_EV
        * HBARC_EV_M**3
    )

    x_length_m = (
        HBARC_EV_M
        / m_x_ev
    )

    print(
        f"M_X_EV={m_x_ev:.15e}"
    )

    print(
        f"M_C_GEV={M_c_gev:.15e}"
    )

    print(
        f"F_SOURCE_GEV={F_gev:.15e}"
    )

    print(
        f"PAYLOAD_MASS_KG={PAYLOAD_MASS_KG:.15e}"
    )

    print(
        f"PAYLOAD_RADIUS_M={payload_radius_m:.15e}"
    )

    print(
        f"PAYLOAD_DENSITY_KG_M3="
        f"{payload_density_kg_m3:.15e}"
    )

    print(
        f"PAYLOAD_TRACE_EV4="
        f"{payload_trace_ev4:.15e}"
    )

    qmod = load_module(
        "qball031d3ar",
        QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a031d3ar",
        D3A_SOURCE,
    )

    old_xmatch = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = X_MATCH

    try:
        print(
            "\n=== STAGE A: RECONSTRUCT CERTIFIED SOURCE ==="
        )

        source_seed = (
            qmod.solve_uncoupled_qball(
                omega_source
            )
        )

        if source_seed is None:
            raise RuntimeError(
                "Failed source seed reconstruction"
            )

        source = qmod.solve_coupled(
            source_seed,
            omega_source,
            epsilon,
            chi_source,
            previous=None,
        )

        if source is None:
            raise RuntimeError(
                "Failed source reconstruction"
            )

        print(
            f"SOURCE_U0="
            f"{float(source.sol(1.0e-5)[2]):.15e}"
        )

        # ----------------------------------------------------------
        # Reconstruct each independent activation profile once.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE B: ACTIVATION PROFILE RECONSTRUCTION ==="
        )

        profiles = {}

        for omega_a in sorted(
            {
                float(
                    row[
                        "omega_activation"
                    ]
                )
                for row
                in inherited
            }
        ):
            solved = (
                qmod.solve_uncoupled_qball(
                    omega_a
                )
            )

            if solved is None:
                raise RuntimeError(
                    "Failed activation profile "
                    f"Omega={omega_a}"
                )

            profiles[
                omega_a
            ] = solved

            print(
                f"PROFILE "
                f"OMEGA={omega_a:.6f} "
                f"A0={float(solved.sol(1.0e-5)[0]):+.12e}"
            )

        # ----------------------------------------------------------
        # Payload sampling coordinates.
        # ----------------------------------------------------------

        radial_nodes, radial_weights = leggauss(
            PAYLOAD_RADIAL_ORDER
        )

        angular_nodes, angular_weights = leggauss(
            PAYLOAD_ANGULAR_ORDER
        )

        payload_s = (
            0.5
            * payload_radius_m
            * (
                radial_nodes
                + 1.0
            )
        )

        payload_ws = (
            0.5
            * payload_radius_m
            * radial_weights
        )

        payload_samples = []

        # Volume samples.
        for (
            s,
            ws,
        ) in zip(
            payload_s,
            payload_ws,
            strict=True,
        ):
            for (
                mu_angle,
                wmu,
            ) in zip(
                angular_nodes,
                angular_weights,
                strict=True,
            ):
                radius_from_source = math.sqrt(
                    payload_center_from_source_m**2
                    + s**2
                    + 2.0
                    * payload_center_from_source_m
                    * s
                    * mu_angle
                )

                weight = (
                    2.0
                    * math.pi
                    * s**2
                    * ws
                    * wmu
                    / payload_volume_m3
                )

                payload_samples.append(
                    (
                        radius_from_source,
                        weight,
                        "volume",
                    )
                )

        # Dense surface samples for maxima.
        for mu_angle in np.linspace(
            -1.0,
            1.0,
            PAYLOAD_SURFACE_POINTS,
        ):
            radius_from_source = math.sqrt(
                payload_center_from_source_m**2
                + payload_radius_m**2
                + 2.0
                * payload_center_from_source_m
                * payload_radius_m
                * float(
                    mu_angle
                )
            )

            payload_samples.append(
                (
                    radius_from_source,
                    0.0,
                    "surface",
                )
            )

        # Center.
        payload_samples.append(
            (
                payload_center_from_source_m,
                0.0,
                "center",
            )
        )

        print(
            f"PAYLOAD_SAMPLE_COUNT="
            f"{len(payload_samples)}"
        )

        # ----------------------------------------------------------
        # Geometry-dependent payload diagnostics, independent of V.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE C: EXACT PAYLOAD ACTIVATION / REACTION SHAPES ==="
        )

        profile_diagnostics = {}

        unique_shapes = sorted(
            {
                (
                    float(
                        row[
                            "omega_activation"
                        ]
                    ),
                    float(
                        row[
                            "mu_mA_over_mX"
                        ]
                    ),
                )
                for row in inherited
            }
        )

        for (
            omega_a,
            mu_ratio,
        ) in unique_shapes:
            solved = profiles[
                omega_a
            ]

            m_a_ev = (
                mu_ratio
                * m_x_ev
            )

            minimum_f = 1.0

            maximum_metric_relerr = 0.0

            maximum_payload_reaction_shape_ev2 = 0.0

            volume_weighted_f = 0.0

            volume_weight_sum = 0.0

            for (
                radius_m,
                weight,
                sample_class,
            ) in payload_samples:
                x = (
                    radius_m
                    / x_length_m
                )

                if x > X_MATCH:
                    raise RuntimeError(
                        "Payload sample exceeded inherited "
                        "source BVP domain"
                    )

                source_state = source.sol(
                    max(
                        x,
                        1.0e-5,
                    )
                )

                u = float(
                    source_state[
                        2
                    ]
                )

                up = float(
                    source_state[
                        3
                    ]
                )

                rho_a = (
                    mu_ratio
                    * x
                )

                a_arr, ap_arr = (
                    d3a.extended_profile(
                        solved,
                        omega_a,
                        np.array(
                            [
                                rho_a
                            ],
                            dtype=float,
                        ),
                    )
                )

                a = float(
                    a_arr[
                        0
                    ]
                )

                ap_rho = float(
                    ap_arr[
                        0
                    ]
                )

                f = float(
                    d3a.activation_fraction(
                        np.array(
                            [
                                a
                            ]
                        )
                    )[0]
                )

                fp = float(
                    d3a.activation_fraction_derivative(
                        np.array(
                            [
                                a
                            ]
                        )
                    )[0]
                )

                minimum_f = min(
                    minimum_f,
                    f,
                )

                if sample_class == "volume":
                    volume_weighted_f += (
                        weight
                        * f
                    )

                    volume_weight_sum += (
                        weight
                    )

                # df/dx.
                da_dx = (
                    mu_ratio
                    * ap_rho
                )

                df_dx = (
                    fp
                    * da_dx
                )

                baseline_dlogA_dx = (
                    -u
                    * up
                )

                activated_dlogA_dx = (
                    -f
                    * u
                    * up
                    -0.5
                    * u**2
                    * df_dx
                )

                metric_relerr = (
                    abs(
                        activated_dlogA_dx
                        - baseline_dlogA_dx
                    )
                    /
                    max(
                        abs(
                            baseline_dlogA_dx
                        ),
                        1.0e-30,
                    )
                )

                maximum_metric_relerr = max(
                    maximum_metric_relerr,
                    metric_relerr,
                )

                intrinsic_shape = (
                    abs(
                        a
                        /
                        (
                            1.0
                            + a**2
                        )
                    )
                    + omega_a**2
                    * abs(
                        a
                    )
                    + 1.0e-30
                )

                # R_payload = shape_eV2 / V^2.
                reaction_shape_ev2 = (
                    0.5
                    * payload_trace_ev4
                    * u**2
                    * abs(
                        fp
                    )
                    /
                    (
                        m_a_ev**2
                        * intrinsic_shape
                    )
                )

                maximum_payload_reaction_shape_ev2 = max(
                    maximum_payload_reaction_shape_ev2,
                    reaction_shape_ev2,
                )

            if volume_weight_sum > 0.0:
                mean_f = (
                    volume_weighted_f
                    / volume_weight_sum
                )
            else:
                mean_f = math.nan

            profile_diagnostics[
                (
                    omega_a,
                    mu_ratio,
                )
            ] = {
                "payload_f_min":
                    minimum_f,

                "payload_f_volume_mean":
                    mean_f,

                "metric_gradient_relerr_max":
                    maximum_metric_relerr,

                "payload_reaction_shape_eV2":
                    maximum_payload_reaction_shape_ev2,
            }

            print(
                f"PAYLOAD_SHAPE "
                f"OMEGA={omega_a:.6f} "
                f"MU={mu_ratio:.9e} "
                f"F_MIN={minimum_f:.12e} "
                f"F_MEAN={mean_f:.12e} "
                f"METRIC_GRAD_RELERR_MAX="
                f"{maximum_metric_relerr:.6e} "
                f"PAYLOAD_REACTION_SHAPE_EV2="
                f"{maximum_payload_reaction_shape_ev2:.6e}"
            )

        # ----------------------------------------------------------
        # EFT/coupling ladder.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE D: METRIC-CUTOFF SENSITIVITY LADDER ==="
        )

        output_rows = []

        ladder_best = {}

        for cutoff_ev in METRIC_CUTOFFS_EV:
            cutoff_rows = []

            V_cutoff_ev = (
                cutoff_ev**2
                / M_c_ev
            )

            for row in inherited:
                omega_a = float(
                    row[
                        "omega_activation"
                    ]
                )

                mu_ratio = float(
                    row[
                        "mu_mA_over_mX"
                    ]
                )

                m_a_ev = float(
                    row[
                        "m_A_eV"
                    ]
                )

                I_E = float(
                    row[
                        "I_E_activation"
                    ]
                )

                I_Q = float(
                    row[
                        "I_Q_activation"
                    ]
                )

                diag = profile_diagnostics[
                    (
                        omega_a,
                        mu_ratio,
                    )
                ]

                V_self_ev = (
                    m_a_ev
                    / math.sqrt(
                        MAX_ACTIVATION_SELF_COUPLING
                    )
                )

                source_reaction_shape = float(
                    row[
                        "reaction_shape"
                    ]
                )

                V_source_reaction_ev = (
                    F_ev
                    * math.sqrt(
                        max(
                            source_reaction_shape,
                            0.0,
                        )
                        /
                        MAX_SOURCE_REACTION_RATIO
                    )
                )

                V_payload_reaction_ev = math.sqrt(
                    max(
                        diag[
                            "payload_reaction_shape_eV2"
                        ],
                        0.0,
                    )
                    /
                    MAX_PAYLOAD_REACTION_RATIO
                )

                V_classical_ev = (
                    m_a_ev
                    * math.sqrt(
                        MIN_CLASSICAL_ACTIVATION_CHARGE
                        /
                        I_Q
                    )
                )

                V_required_ev = max(
                    V_cutoff_ev,
                    V_self_ev,
                    V_source_reaction_ev,
                    V_payload_reaction_ev,
                    V_classical_ev,
                )

                metric_scale_ev = math.sqrt(
                    V_required_ev
                    * M_c_ev
                )

                self_coupling = (
                    m_a_ev**2
                    /
                    V_required_ev**2
                )

                source_reaction_ratio = (
                    (
                        F_ev
                        / V_required_ev
                    )**2
                    * source_reaction_shape
                )

                payload_reaction_ratio = (
                    diag[
                        "payload_reaction_shape_eV2"
                    ]
                    /
                    V_required_ev**2
                )

                activation_energy_ev = (
                    I_E
                    * V_required_ev**2
                    / m_a_ev
                )

                activation_energy_j = (
                    activation_energy_ev
                    * J_PER_EV
                )

                activation_charge = (
                    I_Q
                    * V_required_ev**2
                    / m_a_ev**2
                )

                energy_fraction = (
                    activation_energy_j
                    / operating_energy_j
                )

                geometry_pass = bool(
                    row[
                        "geometry_pass"
                    ]
                )

                bound_pass = bool(
                    row[
                        "bound_pass"
                    ]
                )

                payload_activation_pass = bool(
                    diag[
                        "payload_f_min"
                    ]
                    >= MIN_ACTIVATION_F
                )

                metric_gradient_pass = bool(
                    diag[
                        "metric_gradient_relerr_max"
                    ]
                    <= MAX_METRIC_GRADIENT_RELERR
                )

                reaction_pass = bool(
                    source_reaction_ratio
                    <= MAX_SOURCE_REACTION_RATIO
                    and
                    payload_reaction_ratio
                    <= MAX_PAYLOAD_REACTION_RATIO
                )

                self_coupling_pass = bool(
                    self_coupling
                    <= MAX_ACTIVATION_SELF_COUPLING
                )

                classical_pass = bool(
                    activation_charge
                    >= MIN_CLASSICAL_ACTIVATION_CHARGE
                )

                cutoff_pass = bool(
                    metric_scale_ev
                    >= cutoff_ev
                    * (
                        1.0
                        - 1.0e-12
                    )
                )

                candidate_pass = bool(
                    geometry_pass
                    and
                    bound_pass
                    and
                    payload_activation_pass
                    and
                    metric_gradient_pass
                    and
                    reaction_pass
                    and
                    self_coupling_pass
                    and
                    classical_pass
                    and
                    cutoff_pass
                )

                result = {
                    "cutoff_eV":
                        cutoff_ev,

                    "cutoff_GeV":
                        cutoff_ev
                        / 1.0e9,

                    "omega_activation":
                        omega_a,

                    "mu_mA_over_mX":
                        mu_ratio,

                    "m_A_eV":
                        m_a_ev,

                    "E_over_Qm":
                        float(
                            row[
                                "E_over_Qm"
                            ]
                        ),

                    "f_leak_10m":
                        float(
                            row[
                                "f_leak_10m"
                            ]
                        ),

                    "source_f_min":
                        float(
                            row[
                                "source_f_min"
                            ]
                        ),

                    "payload_f_min":
                        diag[
                            "payload_f_min"
                        ],

                    "payload_f_volume_mean":
                        diag[
                            "payload_f_volume_mean"
                        ],

                    "metric_gradient_relerr_max":
                        diag[
                            "metric_gradient_relerr_max"
                        ],

                    "V_cutoff_eV":
                        V_cutoff_ev,

                    "V_self_eV":
                        V_self_ev,

                    "V_source_reaction_eV":
                        V_source_reaction_ev,

                    "V_payload_reaction_eV":
                        V_payload_reaction_ev,

                    "V_classical_eV":
                        V_classical_ev,

                    "V_required_eV":
                        V_required_ev,

                    "metric_operator_scale_eV":
                        metric_scale_ev,

                    "self_coupling_est":
                        self_coupling,

                    "source_reaction_ratio":
                        source_reaction_ratio,

                    "payload_reaction_ratio":
                        payload_reaction_ratio,

                    "activation_energy_J":
                        activation_energy_j,

                    "activation_energy_GJ":
                        activation_energy_j
                        / 1.0e9,

                    "activation_energy_fraction":
                        energy_fraction,

                    "activation_charge":
                        activation_charge,

                    "candidate_pass":
                        candidate_pass,
                }

                output_rows.append(
                    result
                )

                if candidate_pass:
                    cutoff_rows.append(
                        result
                    )

            if cutoff_rows:
                best = min(
                    cutoff_rows,
                    key=lambda item:
                        float(
                            item[
                                "activation_energy_J"
                            ]
                        ),
                )

                ladder_best[
                    str(
                        cutoff_ev
                    )
                ] = best

                print(
                    f"CUTOFF "
                    f"LAMBDA_GEV={cutoff_ev / 1.0e9:.6e} "
                    f"PASSERS={len(cutoff_rows)} "
                    f"BEST_OMEGA={best['omega_activation']:.6f} "
                    f"BEST_MU={best['mu_mA_over_mX']:.9e} "
                    f"BEST_V_GEV="
                    f"{best['V_required_eV']/1.0e9:.9e} "
                    f"BEST_E_GJ="
                    f"{best['activation_energy_GJ']:.12e} "
                    f"BEST_FRACTION="
                    f"{best['activation_energy_fraction']:.12e} "
                    f"BEST_Q="
                    f"{best['activation_charge']:.12e} "
                    f"PAYLOAD_REACTION="
                    f"{best['payload_reaction_ratio']:.6e} "
                    f"METRIC_GRAD_ERR="
                    f"{best['metric_gradient_relerr_max']:.6e}"
                )

            else:
                ladder_best[
                    str(
                        cutoff_ev
                    )
                ] = None

                print(
                    f"CUTOFF "
                    f"LAMBDA_GEV={cutoff_ev / 1.0e9:.6e} "
                    "PASSERS=0"
                )

        # ----------------------------------------------------------
        # Primary 10-GeV decision.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE E: PRIMARY 10-GEV PREFLIGHT DECISION ==="
        )

        primary = ladder_best[
            str(
                PRIMARY_METRIC_CUTOFF_EV
            )
        ]

        if primary is None:
            primary_pass = False

        else:
            primary_pass = bool(
                primary[
                    "activation_energy_fraction"
                ]
                <= MAX_PRIMARY_ACTIVATION_ENERGY_FRACTION
            )

        if primary is not None:
            optimistic_total_j = (
                operating_energy_j
                + primary[
                    "activation_energy_J"
                ]
            )

            print(
                f"PRIMARY_OMEGA_ACTIVATION="
                f"{primary['omega_activation']:.15e}"
            )

            print(
                f"PRIMARY_MU_MA_OVER_MX="
                f"{primary['mu_mA_over_mX']:.15e}"
            )

            print(
                f"PRIMARY_M_A_EV="
                f"{primary['m_A_eV']:.15e}"
            )

            print(
                f"PRIMARY_V_GEV="
                f"{primary['V_required_eV']/1.0e9:.15e}"
            )

            print(
                f"PRIMARY_METRIC_OPERATOR_SCALE_GEV="
                f"{primary['metric_operator_scale_eV']/1.0e9:.15e}"
            )

            print(
                f"PRIMARY_SELF_COUPLING="
                f"{primary['self_coupling_est']:.15e}"
            )

            print(
                f"PRIMARY_PAYLOAD_F_MIN="
                f"{primary['payload_f_min']:.15e}"
            )

            print(
                f"PRIMARY_METRIC_GRADIENT_RELERR_MAX="
                f"{primary['metric_gradient_relerr_max']:.15e}"
            )

            print(
                f"PRIMARY_SOURCE_REACTION_RATIO="
                f"{primary['source_reaction_ratio']:.15e}"
            )

            print(
                f"PRIMARY_PAYLOAD_REACTION_RATIO="
                f"{primary['payload_reaction_ratio']:.15e}"
            )

            print(
                f"PRIMARY_ACTIVATION_CHARGE="
                f"{primary['activation_charge']:.15e}"
            )

            print(
                f"PRIMARY_ACTIVATION_ENERGY_GJ="
                f"{primary['activation_energy_GJ']:.12f}"
            )

            print(
                f"PRIMARY_ACTIVATION_ENERGY_FRACTION="
                f"{primary['activation_energy_fraction']:.15e}"
            )

            print(
                f"OPTIMISTIC_TOTAL_WITH_ACTIVATION_GJ="
                f"{optimistic_total_j/1.0e9:.12f}"
            )

        else:
            optimistic_total_j = math.nan

        print(
            f"PRIMARY_10GEV_PREFLIGHT_PASS="
            f"{primary_pass}"
        )

        stress_100 = ladder_best[
            str(
                1.0e11
            )
        ]

        if stress_100 is not None:
            print(
                f"STRESS_100GEV_BEST_ACTIVATION_GJ="
                f"{stress_100['activation_energy_GJ']:.12f}"
            )

            print(
                f"STRESS_100GEV_ENERGY_FRACTION="
                f"{stress_100['activation_energy_fraction']:.15e}"
            )

        if primary_pass:
            classification = (
                "GREEN_D3AR_U1_METRIC_ACTIVATION_SURVIVES_"
                "10GEV_EFT_PAYLOAD_REACTION_AND_"
                "INTERIOR_SELF_COUPLING_PREFLIGHT"
            )

            next_action = (
                "031D3B_FULL_FIXED_QX_QY_COUPLED_"
                "X_PHI_Y_METRIC_ACTIVATION_SOLVE"
            )

        elif ladder_best[
            str(
                1.0e9
            )
        ] is not None:
            classification = (
                "YELLOW_D3AR_ACTIVATION_SURVIVES_1GEV_"
                "BUT_NOT_DECLARED_10GEV_PREFLIGHT"
            )

            next_action = (
                "DIAGNOSE_D3_EFT_SCALE_BEFORE_COUPLED_SOLVE"
            )

        else:
            classification = (
                "RED_D3AR_U1_METRIC_ACTIVATION_FAILS_"
                "STRENGTHENED_EFT_OR_PAYLOAD_REACTION_PREFLIGHT"
            )

            next_action = (
                "RERANK_031D_AFTER_D3_ROBUSTNESS_FAILURE"
            )

        print(
            f"031D3AR_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "D3A_ORIGINAL_TINY_ENERGY_QUOTE_PROMOTED=NO"
        )

        print(
            "10GEV_CUTOFF_IS_FINAL_UV_COMPLETION=NO"
        )

        print(
            "100GEV_STRESS_TEST_IS_PROMOTION_REQUIREMENT=NO"
        )

        print(
            "FULL_X_PHI_Y_COUPLED_FIELD_SOLVE=NO"
        )

        print(
            "COUPLED_STABILITY_CLOSED=NO"
        )

        print(
            "CHARGE_INJECTION_RESET_CLOSED=NO"
        )

        print(
            "RADIATION_CLOSED=NO"
        )

        print(
            "FULL_METRIC_BACKREACTION_CLOSED=NO"
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

            "scientific_correction": (
                "The D3A 7.3e-23 J activation quote is not "
                "promoted because the selected point saturated "
                "m_A^2/V^2=4*pi."
            ),

            "primary_metric_cutoff_eV":
                PRIMARY_METRIC_CUTOFF_EV,

            "primary_metric_cutoff_is_final_uv_completion":
                False,

            "payload": {
                "mass_kg":
                    PAYLOAD_MASS_KG,

                "radius_m":
                    payload_radius_m,

                "density_kg_m3":
                    payload_density_kg_m3,

                "trace_eV4":
                    payload_trace_ev4,

                "sample_count":
                    len(
                        payload_samples
                    ),
            },

            "requirements": {
                "max_activation_self_coupling":
                    MAX_ACTIVATION_SELF_COUPLING,

                "max_source_reaction_ratio":
                    MAX_SOURCE_REACTION_RATIO,

                "max_payload_reaction_ratio":
                    MAX_PAYLOAD_REACTION_RATIO,

                "max_metric_gradient_relerr":
                    MAX_METRIC_GRADIENT_RELERR,

                "max_primary_activation_energy_fraction":
                    MAX_PRIMARY_ACTIVATION_ENERGY_FRACTION,

                "min_activation_charge":
                    MIN_CLASSICAL_ACTIVATION_CHARGE,
            },

            "cutoff_best":
                ladder_best,

            "primary":
                primary,

            "claim_limits": [
                (
                    "The 10-GeV metric cutoff is a declared "
                    "pre-D3B robustness diagnostic, not a derived "
                    "UV-completion requirement."
                ),
                (
                    "The 100-GeV result is sensitivity information "
                    "and does not by itself falsify D3."
                ),
                (
                    "Ordinary-payload reaction uses the magnitude "
                    "of the payload rest-energy trace and therefore "
                    "does not credit conformal suppression."
                ),
                (
                    "The activation field is still evaluated on "
                    "the inherited source field rather than in a "
                    "fully coupled X/phi/Y solve."
                ),
                (
                    "Formation/reset and activation charge transport "
                    "remain unclosed."
                ),
                (
                    "Full coupled stability, radiative naturalness, "
                    "physical-metric backreaction and empirical "
                    "fifth-force/EP/PPN closure remain mandatory."
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
                for row in output_rows
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
                output_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"SCAN_CSV={OUT_CSV}"
        )

    finally:
        qmod.X_MATCH = old_xmatch


if __name__ == "__main__":
    main()
