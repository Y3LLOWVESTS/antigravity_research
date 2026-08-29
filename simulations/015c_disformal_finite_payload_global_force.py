r"""Simulation 015C — finite localized source / finite payload COM-force gate.

PURPOSE
-------
Test whether the local total-force reversal reproduced in Simulation 014D can
survive spatial integration over an entire finite passive payload.

This is a substantially stronger operational test than asking whether isolated
grid cells satisfy

    (F_Psi + F_phi) . F_Psi < 0.

SCIENTIFIC QUESTION
-------------------
Can a finite, smooth, compact-support passive payload placed beside a finite,
localized, nonsymmetric matter overdensity acquire a mass-weighted
center-of-mass acceleration pointing away from the source in the same reduced
non-static disformal model used by Simulation 014D?

MODEL
-----
The dynamical scalar-field equations, background cosmology, Poisson solver,
force definitions, numerical evolution method, and health diagnostics are
loaded directly from the byte-preserved Simulation 014D source.

The original 014D density-shape functions are replaced only for this gate by
localized nonsymmetric overdensity families.

The Newtonian peculiar potential is still solved in a periodic cosmological
box. A spatially homogeneous compensating component is required by the
zero-mean periodic Poisson convention. The localized positive perturbation is
the operational source.

The payload is passive and does not enter the source density.

This makes the calculation a finite-test-body limit:

    source -> gravitational/scalar fields -> finite payload

rather than a closed reactionless system.

FORCES
------
Simulation 014D defines

    F_Psi = -grad(Psi) / a^2

and

    F_phi = -(1/2) (xi / g_phi) grad(phi).

The total force per unit passive mass is

    F_total = F_Psi + F_phi.

FINITE PAYLOAD
--------------
The payload weighting function has strict compact support.

For distance r from the payload center and radius R_p,

    w(r) = (1 - r^2/R_p^2)^2,    r < R_p

and

    w(r) = 0,                    r >= R_p.

The mass normalization cancels from the center-of-mass acceleration:

    a_CM =
        integral w F_total dV
        /
        integral w dV.

GLOBAL REVERSAL CRITERION
-------------------------
Let n_hat point from the localized source centroid toward the payload center.

Newtonian attraction requires

    a_Psi,CM . n_hat < 0.

Finite-payload total reversal requires

    a_total,CM . n_hat > 0.

A candidate must also have a meaningful coherent Newtonian source direction so
that a nearly vanishing vector average is not misclassified as reversal.

SOURCE SEARCH
-------------
Three localized asymmetric source families are tested.

Each source is constructed as a compact cluster of unequal Gaussian
overdensities, followed by mean subtraction required by the periodic
cosmological perturbation convention.

The peak density contrast is normalized to the peak contrast of the original
014D deterministic reference density at the same resolution.

DISCOVERY / VALIDATION SEPARATION
---------------------------------
Discovery:

    dimension = 2
    points = 64

and scans:

    source family
    b0
    payload separation
    payload transverse offset
    payload radius

Only root-time results are used for candidate selection.

Validation freezes:

    source family
    b0
    normalized payload offset
    normalized payload radius

and reruns:

    64^2
    96^2
    128^2

plus independently:

    24^3
    32^3
    40^3.

No payload geometry is retuned during refinement.

HEALTH REQUIREMENTS
-------------------
Accepted finite-payload reversal requires:

    min(g_phi) >= 0.10

    min(kinetic denominator) > 0

    max(|Psi|) <= 0.05

in the tested reduced model.

A Newtonian source-force coherence requirement is also imposed to reject
payloads whose apparent sign is caused by cancellation of strong local fields.

SELF-FORCE CONTROL
------------------
The passive payload does not source Psi or phi, so payload self-force is absent
by construction.

As an additional numerical check, the mass-weighted Newtonian self-force of
the positive localized source perturbation is evaluated. It should be small
relative to the mean Newtonian field across the source.

MOMENTUM ACCOUNTING
-------------------
This calculation does not claim reactionless propulsion.

In a complete matter-plus-scalar system, the source and scalar field provide
the reaction/momentum reservoir.

The source backreaction is not dynamically evolved in this reduced gate.

APPROXIMATION LEVEL
-------------------
- reduced non-static disformal scalar model;
- Einstein-de Sitter background;
- weak Newtonian metric potential;
- imposed source density perturbation;
- passive finite test payload;
- periodic computational box;
- numerical approximation.

VALIDATION
----------
The exact SHA-256 of the preserved 014D source is required before execution.

The same 014D run_case implementation is AST-loaded without executing its
top-level historical parameter scans.

The finite-payload result is tested under both 2D and 3D grid refinement.

LIMITATIONS
-----------
A positive result would not establish:

- ordinary baryonic coupling;
- the 014E UV bridge;
- laboratory realizability;
- self-consistent source motion;
- a closed-system center-of-mass acceleration;
- experimental antigravity;
- a practical device.

A positive result would establish only finite passive-payload center-of-mass
force reversal in the stated reduced model and geometry.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_REDUCED_DISFORMAL_FINITE_PASSIVE_PAYLOAD_FORCE_GATE
"""

from __future__ import annotations

import ast
import hashlib
import inspect
import math
import sys
import types
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

SOURCE_014D = (
    ROOT
    / "simulations"
    / "014d_disformal_total_reversal.py"
)

EXPECTED_014D_SHA256 = (
    "01220601e0ed71e84c79c94b36fec7d60"
    "b596572bc192b1ce168dec2db35d71c"
)

GPHI_FLOOR = 0.10
PSI_CEILING = 0.05
KINETIC_FLOOR = 0.0

NEWTONIAN_COHERENCE_FLOOR = 0.20
TOTAL_OUTWARD_COHERENCE_FLOOR = 0.05

DISCOVERY_POINTS = 64
DISCOVERY_B0_VALUES = (
    0.24,
    0.28,
    0.30,
    0.32,
)

SOURCE_KINDS = (
    "TRIPLET",
    "ELONGATED",
    "LOPSIDED_QUAD",
)

VALIDATE_2D_POINTS = (
    64,
    96,
    128,
)

VALIDATE_3D_POINTS = (
    24,
    32,
    40,
)

RUN_CFL = 0.10


_MODEL_NS: dict[str, Any] = {}
_MODEL_TREE: ast.Module | None = None

_ORIGINAL_DENSITY_2D = None
_ORIGINAL_DENSITY_3D = None

_ACTIVE_SOURCE_KIND = "TRIPLET"
_ACTIVE_RUN_ID = ""
_ACTIVE_MODE = "DISCOVERY"

_FIXED_PAYLOAD_OFFSET: tuple[float, float] | None = None
_FIXED_PAYLOAD_RADIUS: float | None = None

_PAYLOAD_RECORDS: list[dict[str, Any]] = []

_GRID_CACHE: dict[
    tuple[int, int],
    tuple[np.ndarray, ...],
] = {}

_WEIGHT_CACHE: dict[
    tuple[
        int,
        int,
        tuple[float, ...],
        float,
    ],
    np.ndarray,
] = {}

_PRINTED_SOURCE_SHAPES: set[
    tuple[str, int, int]
] = set()


def sha256_file(path: Path) -> str:
    """Return SHA-256 digest of a file."""

    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def periodic_delta(
    coordinate: np.ndarray,
    center: float,
) -> np.ndarray:
    """Return shortest signed displacement in a unit periodic box."""

    return (
        coordinate
        - center
        + 0.5
    ) % 1.0 - 0.5


def normalized_grid(
    points: int,
    dimension: int,
) -> tuple[np.ndarray, ...]:
    """Return cached unit-box grid arrays."""

    key = (
        points,
        dimension,
    )

    if key not in _GRID_CACHE:
        coordinate = (
            np.arange(
                points,
                dtype=float,
            )
            / points
        )

        _GRID_CACHE[key] = tuple(
            np.meshgrid(
                *(
                    [coordinate]
                    * dimension
                ),
                indexing="ij",
            )
        )

    return _GRID_CACHE[key]


def source_components(
    kind: str,
    dimension: int,
) -> tuple[
    tuple[
        tuple[float, ...],
        float,
        float,
    ],
    ...,
]:
    """Return localized asymmetric source components.

    Every tuple contains

        center
        amplitude
        Gaussian sigma

    in normalized box coordinates.
    """

    if kind == "TRIPLET":
        components_3d = (
            (
                (0.300, 0.500, 0.500),
                1.00,
                0.060,
            ),
            (
                (0.345, 0.550, 0.525),
                0.58,
                0.042,
            ),
            (
                (0.270, 0.445, 0.465),
                0.34,
                0.034,
            ),
        )

    elif kind == "ELONGATED":
        components_3d = (
            (
                (0.295, 0.500, 0.500),
                1.00,
                0.078,
            ),
            (
                (0.365, 0.525, 0.535),
                0.46,
                0.038,
            ),
            (
                (0.245, 0.465, 0.455),
                0.27,
                0.030,
            ),
        )

    elif kind == "LOPSIDED_QUAD":
        components_3d = (
            (
                (0.300, 0.500, 0.500),
                1.00,
                0.058,
            ),
            (
                (0.352, 0.560, 0.530),
                0.62,
                0.040,
            ),
            (
                (0.255, 0.455, 0.455),
                0.31,
                0.033,
            ),
            (
                (0.320, 0.425, 0.550),
                0.21,
                0.028,
            ),
        )

    else:
        raise ValueError(
            f"Unknown source kind: {kind}"
        )

    result = []

    for (
        center_3d,
        amplitude,
        sigma,
    ) in components_3d:
        result.append(
            (
                tuple(
                    center_3d[
                        :dimension
                    ]
                ),
                amplitude,
                sigma,
            )
        )

    return tuple(result)


def source_centroid(
    kind: str,
    dimension: int,
) -> tuple[float, ...]:
    """Return approximate positive-mass centroid of a source family."""

    components = source_components(
        kind,
        dimension,
    )

    weighted = np.zeros(
        dimension,
        dtype=float,
    )

    total_weight = 0.0

    for (
        center,
        amplitude,
        sigma,
    ) in components:
        weight = (
            amplitude
            * sigma**dimension
        )

        weighted += (
            weight
            * np.asarray(
                center,
                dtype=float,
            )
        )

        total_weight += weight

    return tuple(
        weighted
        / total_weight
    )


def localized_contrast(
    points: int,
    dimension: int,
    kind: str,
) -> np.ndarray:
    """Construct localized asymmetric density contrast.

    The localized Gaussian cluster is mean-subtracted for compatibility with
    the periodic peculiar-Poisson equation.

    Its positive peak is normalized to the positive peak of the original 014D
    deterministic density field at the same resolution.
    """

    if dimension == 2:
        reference = _ORIGINAL_DENSITY_2D(
            points
        )

    elif dimension == 3:
        reference = _ORIGINAL_DENSITY_3D(
            points
        )

    else:
        raise ValueError(
            "dimension must be 2 or 3"
        )

    grids = normalized_grid(
        points,
        dimension,
    )

    raw = np.zeros(
        [points] * dimension,
        dtype=float,
    )

    for (
        center,
        amplitude,
        sigma,
    ) in source_components(
        kind,
        dimension,
    ):
        radius_squared = np.zeros_like(
            raw
        )

        for axis in range(
            dimension
        ):
            delta = periodic_delta(
                grids[axis],
                center[axis],
            )

            radius_squared += (
                delta**2
            )

        raw += (
            amplitude
            * np.exp(
                -0.5
                * radius_squared
                / sigma**2
            )
        )

    contrast = (
        raw
        - float(
            np.mean(
                raw
            )
        )
    )

    target_peak = float(
        np.max(
            reference
        )
    )

    if not (
        target_peak
        > 0.0
    ):
        target_peak = float(
            np.max(
                np.abs(
                    reference
                )
            )
        )

    current_peak = float(
        np.max(
            contrast
        )
    )

    if current_peak <= 0.0:
        raise RuntimeError(
            "localized source has no "
            "positive contrast"
        )

    contrast *= (
        target_peak
        / current_peak
    )

    minimum = float(
        np.min(
            contrast
        )
    )

    if minimum < -0.80:
        contrast *= (
            0.80
            / abs(
                minimum
            )
        )

    key = (
        kind,
        dimension,
        points,
    )

    if key not in _PRINTED_SOURCE_SHAPES:
        _PRINTED_SOURCE_SHAPES.add(
            key
        )

        print(
            "SOURCE_SHAPE "
            f"KIND={kind} "
            f"DIM={dimension} "
            f"POINTS={points} "
            f"MEAN={np.mean(contrast):+.16e} "
            f"MIN={np.min(contrast):+.16e} "
            f"MAX={np.max(contrast):+.16e} "
            f"ONE_PLUS_MIN="
            f"{1.0 + np.min(contrast):+.16e}"
        )

    return contrast


def density_shape_2d_015c(
    points: int,
) -> np.ndarray:
    """Return active localized 2D source."""

    return localized_contrast(
        points,
        2,
        _ACTIVE_SOURCE_KIND,
    )


def density_shape_3d_015c(
    points: int,
) -> np.ndarray:
    """Return active localized 3D source."""

    return localized_contrast(
        points,
        3,
        _ACTIVE_SOURCE_KIND,
    )


def payload_weight(
    points: int,
    dimension: int,
    center: tuple[float, ...],
    radius: float,
) -> np.ndarray:
    """Return smooth compact-support finite-payload weight."""

    cache_key = (
        points,
        dimension,
        tuple(
            round(
                value,
                12,
            )
            for value in center
        ),
        round(
            radius,
            12,
        ),
    )

    if cache_key in _WEIGHT_CACHE:
        return _WEIGHT_CACHE[
            cache_key
        ]

    grids = normalized_grid(
        points,
        dimension,
    )

    radius_squared = np.zeros(
        [points] * dimension,
        dtype=float,
    )

    for axis in range(
        dimension
    ):
        delta = periodic_delta(
            grids[axis],
            center[axis],
        )

        radius_squared += (
            delta**2
        )

    normalized_radius_squared = (
        radius_squared
        / radius**2
    )

    weight = np.where(
        normalized_radius_squared
        < 1.0,
        (
            1.0
            - normalized_radius_squared
        )**2,
        0.0,
    )

    _WEIGHT_CACHE[
        cache_key
    ] = weight

    return weight


def candidate_payloads(
    dimension: int,
) -> list[
    tuple[
        tuple[float, ...],
        tuple[float, float],
        float,
    ]
]:
    """Return discovery or frozen validation payloads."""

    source_center = np.asarray(
        source_centroid(
            _ACTIVE_SOURCE_KIND,
            dimension,
        ),
        dtype=float,
    )

    if (
        _ACTIVE_MODE
        == "FIXED"
    ):
        if (
            _FIXED_PAYLOAD_OFFSET
            is None
            or _FIXED_PAYLOAD_RADIUS
            is None
        ):
            raise RuntimeError(
                "fixed payload geometry "
                "was not initialized"
            )

        offset = np.zeros(
            dimension,
            dtype=float,
        )

        offset[0] = (
            _FIXED_PAYLOAD_OFFSET[0]
        )

        offset[1] = (
            _FIXED_PAYLOAD_OFFSET[1]
        )

        center = (
            source_center
            + offset
        ) % 1.0

        return [
            (
                tuple(
                    center
                ),
                _FIXED_PAYLOAD_OFFSET,
                _FIXED_PAYLOAD_RADIUS,
            )
        ]

    payloads = []

    for dx in (
        0.20,
        0.24,
        0.28,
        0.32,
    ):
        for dy in (
            -0.06,
            0.0,
            0.06,
        ):
            for radius in (
                0.08,
                0.10,
                0.12,
                0.14,
            ):
                offset = np.zeros(
                    dimension,
                    dtype=float,
                )

                offset[0] = dx
                offset[1] = dy

                center = (
                    source_center
                    + offset
                ) % 1.0

                payloads.append(
                    (
                        tuple(
                            center
                        ),
                        (
                            dx,
                            dy,
                        ),
                        radius,
                    )
                )

    return payloads


def weighted_vector(
    weight: np.ndarray,
    components: list[np.ndarray],
) -> np.ndarray:
    """Return payload-mass-weighted vector average."""

    denominator = float(
        np.sum(
            weight
        )
    )

    if denominator <= 0.0:
        return np.full(
            len(
                components
            ),
            np.nan,
        )

    return np.asarray(
        [
            float(
                np.sum(
                    weight
                    * component
                )
                / denominator
            )
            for component in components
        ],
        dtype=float,
    )


def weighted_mean_magnitude(
    weight: np.ndarray,
    components: list[np.ndarray],
) -> float:
    """Return weighted mean local force magnitude."""

    denominator = float(
        np.sum(
            weight
        )
    )

    if denominator <= 0.0:
        return math.nan

    magnitude_squared = np.zeros_like(
        weight
    )

    for component in components:
        magnitude_squared += (
            component**2
        )

    return float(
        np.sum(
            weight
            * np.sqrt(
                magnitude_squared
            )
        )
        / denominator
    )


def source_newtonian_self_force_ratio(
    points: int,
    dimension: int,
    newton_components: list[np.ndarray],
) -> float:
    """Return normalized Newtonian source self-force residual."""

    contrast = localized_contrast(
        points,
        dimension,
        _ACTIVE_SOURCE_KIND,
    )

    source_weight = np.maximum(
        contrast,
        0.0,
    )

    source_cm = weighted_vector(
        source_weight,
        newton_components,
    )

    mean_field = weighted_mean_magnitude(
        source_weight,
        newton_components,
    )

    return float(
        np.linalg.norm(
            source_cm
        )
        / (
            mean_field
            + 1.0e-30
        )
    )


def payload_scan(
    *,
    time: float,
    dimension: int,
    points: int,
    B0: float,
    psi: np.ndarray,
    newton_components: list[np.ndarray],
    fifth_components: list[np.ndarray],
    g_phi: np.ndarray,
    kinetic_denominator: np.ndarray,
) -> None:
    """Evaluate finite-payload center-of-mass force candidates."""

    total_components = [
        newton
        + fifth
        for (
            newton,
            fifth,
        ) in zip(
            newton_components,
            fifth_components,
        )
    ]

    source_center = np.asarray(
        source_centroid(
            _ACTIVE_SOURCE_KIND,
            dimension,
        ),
        dtype=float,
    )

    minimum_g_phi = float(
        np.min(
            g_phi
        )
    )

    minimum_kinetic = float(
        np.min(
            kinetic_denominator
        )
    )

    maximum_abs_psi = float(
        np.max(
            np.abs(
                psi
            )
        )
    )

    source_self_force_ratio = (
        source_newtonian_self_force_ratio(
            points,
            dimension,
            newton_components,
        )
    )

    for (
        center,
        offset_2d,
        radius,
    ) in candidate_payloads(
        dimension
    ):
        center_array = np.asarray(
            center,
            dtype=float,
        )

        radial_vector = (
            center_array
            - source_center
            + 0.5
        ) % 1.0 - 0.5

        radial_norm = float(
            np.linalg.norm(
                radial_vector
            )
        )

        if radial_norm <= 0.0:
            continue

        outward_hat = (
            radial_vector
            / radial_norm
        )

        weight = payload_weight(
            points,
            dimension,
            center,
            radius,
        )

        if float(
            np.sum(
                weight
            )
        ) <= 0.0:
            continue

        newton_cm = weighted_vector(
            weight,
            newton_components,
        )

        fifth_cm = weighted_vector(
            weight,
            fifth_components,
        )

        total_cm = (
            newton_cm
            + fifth_cm
        )

        newton_out = float(
            np.dot(
                newton_cm,
                outward_hat,
            )
        )

        fifth_out = float(
            np.dot(
                fifth_cm,
                outward_hat,
            )
        )

        total_out = float(
            np.dot(
                total_cm,
                outward_hat,
            )
        )

        mean_newton = (
            weighted_mean_magnitude(
                weight,
                newton_components,
            )
        )

        mean_total = (
            weighted_mean_magnitude(
                weight,
                total_components,
            )
        )

        newton_coherence = float(
            -newton_out
            / (
                mean_newton
                + 1.0e-30
            )
        )

        total_outward_coherence = float(
            total_out
            / (
                mean_total
                + 1.0e-30
            )
        )

        meaningful_newton = bool(
            newton_out
            < 0.0
            and newton_coherence
            >= NEWTONIAN_COHERENCE_FLOOR
            and mean_newton
            > 1.0e-12
        )

        safe = bool(
            minimum_g_phi
            >= GPHI_FLOOR
            and minimum_kinetic
            > KINETIC_FLOOR
            and maximum_abs_psi
            <= PSI_CEILING
        )

        global_reversal = bool(
            safe
            and meaningful_newton
            and total_out
            > 0.0
            and total_outward_coherence
            >= TOTAL_OUTWARD_COHERENCE_FLOOR
        )

        if meaningful_newton:
            reversal_margin = float(
                total_out
                / (
                    -newton_out
                    + 1.0e-30
                )
            )

        else:
            reversal_margin = (
                -math.inf
            )

        _PAYLOAD_RECORDS.append(
            {
                "run_id":
                    _ACTIVE_RUN_ID,
                "source_kind":
                    _ACTIVE_SOURCE_KIND,
                "B0":
                    float(
                        B0
                    ),
                "dimension":
                    int(
                        dimension
                    ),
                "points":
                    int(
                        points
                    ),
                "time":
                    float(
                        time
                    ),
                "center":
                    tuple(
                        float(
                            value
                        )
                        for value in center
                    ),
                "offset":
                    (
                        float(
                            offset_2d[0]
                        ),
                        float(
                            offset_2d[1]
                        ),
                    ),
                "radius":
                    float(
                        radius
                    ),
                "newton_out":
                    newton_out,
                "fifth_out":
                    fifth_out,
                "total_out":
                    total_out,
                "newton_coherence":
                    newton_coherence,
                "total_outward_coherence":
                    total_outward_coherence,
                "mean_newton":
                    mean_newton,
                "mean_total":
                    mean_total,
                "minimum_g_phi":
                    minimum_g_phi,
                "minimum_kinetic":
                    minimum_kinetic,
                "maximum_abs_psi":
                    maximum_abs_psi,
                "source_self_force_ratio":
                    source_self_force_ratio,
                "safe":
                    safe,
                "meaningful_newton":
                    meaningful_newton,
                "global_reversal":
                    global_reversal,
                "reversal_margin":
                    reversal_margin,
            }
        )


class PayloadInjector(
    ast.NodeTransformer
):
    """Inject payload diagnostics into 014D run_case.metrics."""

    def visit_FunctionDef(
        self,
        node: ast.FunctionDef,
    ) -> ast.AST:
        if node.name != "run_case":
            return self.generic_visit(
                node
            )

        metrics_node = None

        for statement in node.body:
            if (
                isinstance(
                    statement,
                    ast.FunctionDef,
                )
                and statement.name
                == "metrics"
            ):
                metrics_node = statement
                break

        if metrics_node is None:
            raise RuntimeError(
                "Could not locate nested "
                "run_case.metrics"
            )

        injected = False
        new_body = []

        for statement in metrics_node.body:
            if (
                isinstance(
                    statement,
                    ast.Return,
                )
                and not injected
            ):
                call = ast.Expr(
                    value=ast.Call(
                        func=ast.Name(
                            id="_015C_payload_scan",
                            ctx=ast.Load(),
                        ),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg="time",
                                value=ast.Name(
                                    id="time",
                                    ctx=ast.Load(),
                                ),
                            ),
                            ast.keyword(
                                arg="dimension",
                                value=ast.Name(
                                    id="dimension",
                                    ctx=ast.Load(),
                                ),
                            ),
                            ast.keyword(
                                arg="points",
                                value=ast.Name(
                                    id="points",
                                    ctx=ast.Load(),
                                ),
                            ),
                            ast.keyword(
                                arg="B0",
                                value=ast.Name(
                                    id="B0",
                                    ctx=ast.Load(),
                                ),
                            ),
                            ast.keyword(
                                arg="psi",
                                value=ast.Name(
                                    id="psi",
                                    ctx=ast.Load(),
                                ),
                            ),
                            ast.keyword(
                                arg="newton_components",
                                value=ast.Name(
                                    id="newton_components",
                                    ctx=ast.Load(),
                                ),
                            ),
                            ast.keyword(
                                arg="fifth_components",
                                value=ast.Name(
                                    id="fifth_components",
                                    ctx=ast.Load(),
                                ),
                            ),
                            ast.keyword(
                                arg="g_phi",
                                value=ast.Name(
                                    id="g_phi",
                                    ctx=ast.Load(),
                                ),
                            ),
                            ast.keyword(
                                arg="kinetic_denominator",
                                value=ast.Name(
                                    id="kinetic_denominator",
                                    ctx=ast.Load(),
                                ),
                            ),
                        ],
                    )
                )

                ast.copy_location(
                    call,
                    statement,
                )

                new_body.append(
                    call
                )

                injected = True

            new_body.append(
                statement
            )

        if not injected:
            raise RuntimeError(
                "Could not locate direct "
                "return in metrics()"
            )

        metrics_node.body = new_body

        return node


def load_014d_model() -> tuple[
    dict[str, Any],
    ast.Module,
]:
    """Load 014D definitions without executing historical top-level runs."""

    actual_hash = sha256_file(
        SOURCE_014D
    )

    print(
        "014D_SHA256="
        f"{actual_hash}"
    )

    print(
        "014D_HASH_MATCH="
        f"{actual_hash == EXPECTED_014D_SHA256}"
    )

    if (
        actual_hash
        != EXPECTED_014D_SHA256
    ):
        raise RuntimeError(
            "014D source hash mismatch"
        )

    source = SOURCE_014D.read_text()
    tree = ast.parse(
        source
    )

    print_run_nodes = [
        node
        for node in tree.body
        if (
            isinstance(
                node,
                ast.FunctionDef,
            )
            and node.name
            == "print_run"
        )
    ]

    if len(
        print_run_nodes
    ) != 1:
        raise RuntimeError(
            "Unable to identify "
            "014D definition boundary"
        )

    cutoff_line = int(
        print_run_nodes[0]
        .end_lineno
        or print_run_nodes[0]
        .lineno
    )

    selected_body = [
        node
        for node in tree.body
        if int(
            getattr(
                node,
                "lineno",
                0,
            )
        )
        <= cutoff_line
    ]

    model_tree = ast.Module(
        body=selected_body,
        type_ignores=[],
    )

    model_tree = PayloadInjector().visit(
        model_tree
    )

    ast.fix_missing_locations(
        model_tree
    )

    module_name = (
        "_ag014d_015c_model"
    )

    module = types.ModuleType(
        module_name
    )

    module.__file__ = str(
        SOURCE_014D
    )

    module.__dict__[
        "_015C_payload_scan"
    ] = payload_scan

    sys.modules[
        module_name
    ] = module

    namespace: dict[str, Any] = (
        module.__dict__
    )

    exec(
        compile(
            model_tree,
            str(
                SOURCE_014D
            ),
            "exec",
        ),
        namespace,
        namespace,
    )

    return (
        namespace,
        tree,
    )


def configure_model_namespace() -> None:
    """Install 015C density functions into the loaded 014D namespace."""

    global _ORIGINAL_DENSITY_2D
    global _ORIGINAL_DENSITY_3D

    _ORIGINAL_DENSITY_2D = (
        _MODEL_NS[
            "density_shape_2d"
        ]
    )

    _ORIGINAL_DENSITY_3D = (
        _MODEL_NS[
            "density_shape_3d"
        ]
    )

    _MODEL_NS[
        "density_shape_2d"
    ] = density_shape_2d_015c

    _MODEL_NS[
        "density_shape_3d"
    ] = density_shape_3d_015c

    _MODEL_NS[
        "_015C_payload_scan"
    ] = payload_scan


def run_case_kwargs(
    *,
    B0: float,
    dimension: int,
    points: int,
) -> dict[str, Any]:
    """Construct kwargs for the preserved run_case signature."""

    run_case = _MODEL_NS[
        "run_case"
    ]

    signature = inspect.signature(
        run_case
    )

    kwargs: dict[str, Any] = {}

    for (
        name,
        parameter,
    ) in signature.parameters.items():
        lowered = name.lower()

        if lowered == "b0":
            kwargs[name] = B0

        elif lowered == "dimension":
            kwargs[name] = dimension

        elif lowered == "points":
            kwargs[name] = points

        elif lowered == "cfl":
            kwargs[name] = RUN_CFL

        elif (
            parameter.default
            is not inspect._empty
        ):
            continue

        else:
            raise RuntimeError(
                "015C does not know how "
                "to populate required "
                f"run_case parameter {name!r}; "
                f"signature={signature}"
            )

    return kwargs


def root_records_for_run(
    run_id: str,
    root_time: float,
) -> list[dict[str, Any]]:
    """Return payload records evaluated at the background root time."""

    tolerance = max(
        1.0e-10,
        1.0e-8
        * max(
            1.0,
            abs(
                root_time
            ),
        ),
    )

    return [
        record
        for record in _PAYLOAD_RECORDS
        if (
            record[
                "run_id"
            ]
            == run_id
            and abs(
                record[
                    "time"
                ]
                - root_time
            )
            <= tolerance
        )
    ]


def best_root_record(
    run_id: str,
    root_time: float,
) -> dict[str, Any] | None:
    """Return best meaningful root-time payload for one run."""

    records = root_records_for_run(
        run_id,
        root_time,
    )

    if not records:
        return None

    meaningful = [
        record
        for record in records
        if record[
            "meaningful_newton"
        ]
    ]

    if meaningful:
        return max(
            meaningful,
            key=lambda record:
                record[
                    "reversal_margin"
                ],
        )

    return max(
        records,
        key=lambda record:
            record[
                "total_out"
            ],
    )


def print_payload_record(
    prefix: str,
    record: dict[str, Any] | None,
) -> None:
    """Print one payload record in machine-readable form."""

    if record is None:
        print(
            f"{prefix}=NO_RECORD"
        )
        return

    print(
        f"{prefix} "
        f"RUN={record['run_id']} "
        f"SOURCE={record['source_kind']} "
        f"B0={record['B0']:.8f} "
        f"DIM={record['dimension']} "
        f"POINTS={record['points']} "
        f"TIME={record['time']:.16e} "
        f"OFFSET_X={record['offset'][0]:+.8f} "
        f"OFFSET_Y={record['offset'][1]:+.8f} "
        f"RADIUS={record['radius']:.8f} "
        f"NEWTON_OUT={record['newton_out']:+.16e} "
        f"FIFTH_OUT={record['fifth_out']:+.16e} "
        f"TOTAL_OUT={record['total_out']:+.16e} "
        f"REVERSAL_MARGIN="
        f"{record['reversal_margin']:+.16e} "
        f"NEWTON_COHERENCE="
        f"{record['newton_coherence']:+.16e} "
        f"TOTAL_OUT_COHERENCE="
        f"{record['total_outward_coherence']:+.16e} "
        f"MIN_GPHI={record['minimum_g_phi']:.16e} "
        f"MIN_KIN={record['minimum_kinetic']:.16e} "
        f"MAX_ABS_PSI={record['maximum_abs_psi']:.16e} "
        f"SOURCE_SELF_FORCE_RATIO="
        f"{record['source_self_force_ratio']:.16e} "
        f"SAFE={record['safe']} "
        f"GLOBAL_REVERSAL={record['global_reversal']}"
    )


def execute_case(
    *,
    B0: float,
    dimension: int,
    points: int,
    source_kind: str,
    run_id: str,
) -> tuple[
    Any | None,
    dict[str, Any] | None,
]:
    """Execute one preserved-model case and return best root payload."""

    global _ACTIVE_SOURCE_KIND
    global _ACTIVE_RUN_ID

    _ACTIVE_SOURCE_KIND = (
        source_kind
    )

    _ACTIVE_RUN_ID = run_id

    kwargs = run_case_kwargs(
        B0=B0,
        dimension=dimension,
        points=points,
    )

    print(
        "RUN_START "
        f"ID={run_id} "
        f"SOURCE={source_kind} "
        f"B0={B0:.8f} "
        f"DIM={dimension} "
        f"POINTS={points} "
        f"KWARGS={kwargs}"
    )

    try:
        result = _MODEL_NS[
            "run_case"
        ](
            **kwargs
        )

    except Exception as exc:
        print(
            "RUN_EXCEPTION "
            f"ID={run_id} "
            f"TYPE={type(exc).__name__} "
            f"MESSAGE={exc}"
        )

        return (
            None,
            None,
        )

    root_record = best_root_record(
        run_id,
        float(
            result.root_time
        ),
    )

    print_payload_record(
        "RUN_ROOT_BEST",
        root_record,
    )

    print(
        "RUN_HEALTH "
        f"ID={run_id} "
        f"ROOT_MIN_GPHI="
        f"{result.root_metrics.minimum_g_phi:.16e} "
        f"ROOT_MIN_KIN="
        f"{result.root_metrics.minimum_kinetic_denominator:.16e} "
        f"ROOT_MAX_ABS_PSI="
        f"{result.root_metrics.maximum_abs_psi:.16e} "
        f"ORIGINAL_LOCAL_REVERSAL_FRAC="
        f"{result.root_metrics.total_reversal_fraction:.16e}"
    )

    return (
        result,
        root_record,
    )


def relative_change(
    a: float,
    b: float,
) -> float:
    """Return symmetric relative difference."""

    scale = max(
        abs(
            a
        ),
        abs(
            b
        ),
        1.0e-30,
    )

    return abs(
        a
        - b
    ) / scale


def main() -> None:
    """Execute discovery and frozen-geometry validation."""

    global _MODEL_NS
    global _MODEL_TREE

    global _ACTIVE_MODE
    global _FIXED_PAYLOAD_OFFSET
    global _FIXED_PAYLOAD_RADIUS

    print(
        "=== 015C — FINITE SOURCE / "
        "FINITE PAYLOAD GLOBAL FORCE GATE ==="
    )

    (
        _MODEL_NS,
        _MODEL_TREE,
    ) = load_014d_model()

    configure_model_namespace()

    run_case = _MODEL_NS[
        "run_case"
    ]

    print(
        "014D_RUN_CASE_SIGNATURE="
        f"{inspect.signature(run_case)}"
    )

    print()
    print(
        "=== DISCOVERY: FINITE SOURCE / "
        "FINITE PAYLOAD 2D ROOT-TIME SCAN ==="
    )

    _ACTIVE_MODE = "DISCOVERY"

    discovery_records = []

    for source_kind in SOURCE_KINDS:
        for B0 in DISCOVERY_B0_VALUES:
            run_id = (
                "DISC_"
                f"{source_kind}_"
                f"B{B0:.2f}"
            )

            (
                result,
                record,
            ) = execute_case(
                B0=B0,
                dimension=2,
                points=DISCOVERY_POINTS,
                source_kind=source_kind,
                run_id=run_id,
            )

            if (
                result is not None
                and record is not None
            ):
                discovery_records.append(
                    record
                )

    qualifying_discovery = [
        record
        for record in discovery_records
        if record[
            "global_reversal"
        ]
    ]

    print()
    print(
        "DISCOVERY_COMPLETED_CASES="
        f"{len(discovery_records)}"
    )

    print(
        "DISCOVERY_SAFE_GLOBAL_REVERSAL_CASES="
        f"{len(qualifying_discovery)}"
    )

    if qualifying_discovery:
        winner = max(
            qualifying_discovery,
            key=lambda record: (
                record[
                    "reversal_margin"
                ],
                record[
                    "total_outward_coherence"
                ],
            ),
        )

        print_payload_record(
            "DISCOVERY_WINNER",
            winner,
        )

    else:
        meaningful = [
            record
            for record in discovery_records
            if record[
                "meaningful_newton"
            ]
        ]

        if meaningful:
            best_failed = max(
                meaningful,
                key=lambda record:
                    record[
                        "reversal_margin"
                    ],
            )

        elif discovery_records:
            best_failed = max(
                discovery_records,
                key=lambda record:
                    record[
                        "total_out"
                    ],
            )

        else:
            best_failed = None

        print_payload_record(
            "DISCOVERY_BEST_FAILED_CASE",
            best_failed,
        )

        print()
        print(
            "015C_FINITE_PAYLOAD_DISCOVERY="
            "NO_SAFE_GLOBAL_REVERSAL_IN_TESTED_DOMAIN"
        )

        print(
            "GLOBAL_BODY_REPULSION="
            "NOT_ESTABLISHED"
        )

        print(
            "014D_LOCAL_REVERSAL_RESULT="
            "PRESERVED"
        )

        print(
            "INTERPRETATION="
            "LOCAL_REVERSAL_DID_NOT_YET_SURVIVE_"
            "FINITE_PASSIVE_PAYLOAD_INTEGRATION_"
            "FOR_TESTED_LOCALIZED_SOURCE_FAMILIES"
        )

        print(
            "NEXT="
            "DEMOTE_DIRECT_DISFORMAL_PRACTICAL_ROUTE_"
            "AND_RETURN_TO_STRUCTURALLY_SEQUESTERED_"
            "SOURCE_REFERENCED_COLLECTIVE_FORCE"
        )

        print(
            "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
        )

        return

    _FIXED_PAYLOAD_OFFSET = (
        winner[
            "offset"
        ]
    )

    _FIXED_PAYLOAD_RADIUS = float(
        winner[
            "radius"
        ]
    )

    selected_source = str(
        winner[
            "source_kind"
        ]
    )

    selected_B0 = float(
        winner[
            "B0"
        ]
    )

    _ACTIVE_MODE = "FIXED"

    print()
    print(
        "=== FROZEN GEOMETRY ==="
    )

    print(
        "FROZEN_SOURCE_KIND="
        f"{selected_source}"
    )

    print(
        "FROZEN_B0="
        f"{selected_B0:.16e}"
    )

    print(
        "FROZEN_PAYLOAD_OFFSET_X="
        f"{_FIXED_PAYLOAD_OFFSET[0]:+.16e}"
    )

    print(
        "FROZEN_PAYLOAD_OFFSET_Y="
        f"{_FIXED_PAYLOAD_OFFSET[1]:+.16e}"
    )

    print(
        "FROZEN_PAYLOAD_RADIUS="
        f"{_FIXED_PAYLOAD_RADIUS:.16e}"
    )

    validation_2d = []

    print()
    print(
        "=== 2D FROZEN-GEOMETRY REFINEMENT ==="
    )

    for points in VALIDATE_2D_POINTS:
        run_id = (
            "VAL2D_"
            f"{points}"
        )

        (
            result,
            record,
        ) = execute_case(
            B0=selected_B0,
            dimension=2,
            points=points,
            source_kind=selected_source,
            run_id=run_id,
        )

        if (
            result is not None
            and record is not None
        ):
            validation_2d.append(
                record
            )

    validation_3d = []

    print()
    print(
        "=== 3D FROZEN-GEOMETRY REFINEMENT ==="
    )

    for points in VALIDATE_3D_POINTS:
        run_id = (
            "VAL3D_"
            f"{points}"
        )

        (
            result,
            record,
        ) = execute_case(
            B0=selected_B0,
            dimension=3,
            points=points,
            source_kind=selected_source,
            run_id=run_id,
        )

        if (
            result is not None
            and record is not None
        ):
            validation_3d.append(
                record
            )

    all_2d_present = (
        len(
            validation_2d
        )
        == len(
            VALIDATE_2D_POINTS
        )
    )

    all_3d_present = (
        len(
            validation_3d
        )
        == len(
            VALIDATE_3D_POINTS
        )
    )

    all_2d_reversed = bool(
        all_2d_present
        and all(
            record[
                "global_reversal"
            ]
            for record in validation_2d
        )
    )

    all_3d_reversed = bool(
        all_3d_present
        and all(
            record[
                "global_reversal"
            ]
            for record in validation_3d
        )
    )

    print()
    print(
        "=== CONVERGENCE SUMMARY ==="
    )

    print(
        "2D_VALIDATION_COMPLETE="
        f"{all_2d_present}"
    )

    print(
        "3D_VALIDATION_COMPLETE="
        f"{all_3d_present}"
    )

    print(
        "2D_FINITE_PAYLOAD_REVERSAL_SIGN_STABLE="
        f"{all_2d_reversed}"
    )

    print(
        "3D_FINITE_PAYLOAD_REVERSAL_SIGN_STABLE="
        f"{all_3d_reversed}"
    )

    if len(
        validation_2d
    ) >= 2:
        print(
            "2D_HIGH_GRID_TOTAL_OUT_REL_CHANGE="
            f"{relative_change(
                validation_2d[-1]['total_out'],
                validation_2d[-2]['total_out'],
            ):.16e}"
        )

    if len(
        validation_3d
    ) >= 2:
        print(
            "3D_HIGH_GRID_TOTAL_OUT_REL_CHANGE="
            f"{relative_change(
                validation_3d[-1]['total_out'],
                validation_3d[-2]['total_out'],
            ):.16e}"
        )

    validated_records = (
        validation_2d
        + validation_3d
    )

    if validated_records:
        min_g_phi = min(
            record[
                "minimum_g_phi"
            ]
            for record in validated_records
        )

        min_kinetic = min(
            record[
                "minimum_kinetic"
            ]
            for record in validated_records
        )

        max_psi = max(
            record[
                "maximum_abs_psi"
            ]
            for record in validated_records
        )

        max_source_self_force_ratio = max(
            record[
                "source_self_force_ratio"
            ]
            for record in validated_records
        )

    else:
        min_g_phi = math.nan
        min_kinetic = math.nan
        max_psi = math.nan
        max_source_self_force_ratio = (
            math.nan
        )

    print(
        "VALIDATED_MIN_GPHI="
        f"{min_g_phi:.16e}"
    )

    print(
        "VALIDATED_MIN_KINETIC_DENOMINATOR="
        f"{min_kinetic:.16e}"
    )

    print(
        "VALIDATED_MAX_ABS_PSI="
        f"{max_psi:.16e}"
    )

    print(
        "MAX_NEWTONIAN_SOURCE_SELF_FORCE_RATIO="
        f"{max_source_self_force_ratio:.16e}"
    )

    health_green = bool(
        validated_records
        and min_g_phi
        >= GPHI_FLOOR
        and min_kinetic
        > KINETIC_FLOOR
        and max_psi
        <= PSI_CEILING
    )

    finite_payload_gate = bool(
        all_2d_reversed
        and all_3d_reversed
        and health_green
    )

    print()
    print(
        "=== 015C DECISION ==="
    )

    print(
        "FINITE_LOCALIZED_SOURCE="
        "YES"
    )

    print(
        "FINITE_COMPACT_SUPPORT_PAYLOAD="
        "YES"
    )

    print(
        "PAYLOAD_INCLUDED_IN_FIELD_SOURCE="
        "NO"
    )

    print(
        "PAYLOAD_SELF_FORCE="
        "ABSENT_BY_TEST_BODY_CONSTRUCTION"
    )

    print(
        "NEWTONIAN_SOURCE_ATTRACTION_REQUIRED="
        "YES"
    )

    print(
        "HEALTH_GATE_GREEN="
        f"{health_green}"
    )

    print(
        "FINITE_PASSIVE_PAYLOAD_COM_REVERSAL="
        f"{finite_payload_gate}"
    )

    if finite_payload_gate:
        print(
            "PROJECT_REPRODUCED_FINITE_PAYLOAD_"
            "CENTER_OF_MASS_REVERSAL="
            "YES_IN_CONTROLLED_REDUCED_"
            "DISFORMAL_TEST_BODY_MODEL"
        )

        print(
            "014D_RESULT_PROMOTED_FROM="
            "LOCAL_CELL_REVERSAL"
        )

        print(
            "014D_RESULT_PROMOTED_TO="
            "FINITE_PASSIVE_PAYLOAD_COM_REVERSAL_"
            "IN_TESTED_REDUCED_MODEL"
        )

        print(
            "GLOBAL_CLOSED_SYSTEM_LIFT="
            "NOT_ESTABLISHED"
        )

        print(
            "ORDINARY_BARYONIC_REALIZATION="
            "NOT_ESTABLISHED"
        )

        print(
            "NEXT="
            "015D_INDEPENDENT_PSEUDOSPECTRAL_OR_"
            "RK4_REPRODUCTION_PLUS_SOURCE_"
            "REACTION_MOMENTUM_ACCOUNTING"
        )

    else:
        print(
            "PROJECT_REPRODUCED_FINITE_PAYLOAD_"
            "CENTER_OF_MASS_REVERSAL="
            "NO_IN_FULL_VALIDATION_GATE"
        )

        print(
            "014D_LOCAL_CELL_REVERSAL="
            "PRESERVED"
        )

        print(
            "DIRECT_DISFORMAL_PRACTICAL_PRIORITY="
            "DEMOTED"
        )

        print(
            "NEXT="
            "STRUCTURALLY_SEQUESTERED_"
            "SOURCE_REFERENCED_COLLECTIVE_"
            "FIFTH_FORCE_UV_SEARCH"
        )

    print(
        "REACTIONLESS_PROPULSION="
        "NO_CLAIM"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_REDUCED_DISFORMAL_"
        "FINITE_PASSIVE_PAYLOAD_FORCE_GATE"
    )


if __name__ == "__main__":
    main()
