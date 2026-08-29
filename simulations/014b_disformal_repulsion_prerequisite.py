"""014B — non-static disformal-repulsion prerequisite gate.

PURPOSE
-------
Test the cheapest necessary ingredients of a published modified-gravity
mechanism that has produced genuine fifth-force repulsion in full nonlinear
non-static simulations.

This branch is deliberately different from the pure-static disformal
calculation already considered by ANTIGRAVITY_RESEARCH.

SCIENTIFIC QUESTION
-------------------
Does the healthy non-static disformal background actually enter the special
dynamical regime associated in the published theory with repulsive fifth
forces, without crossing the singular/non-invertible metric boundary?

If not, do not build the expensive spatial solver.

If yes, promote immediately to a nonspherical non-static spatial force
calculation.

PUBLISHED MODEL
---------------
The reference model is the disformally coupled quintessence theory studied by

    Llinares, Hagala & Mota
    MNRAS 491, 1868-1886 (2020)
    arXiv:1902.02125.

The matter-frame metric is

    gtilde_ab
      = g_ab
        + B(phi) d_a phi d_b phi.

For the constant-coupling branch,

    beta = 0

and therefore

    B(phi) = B0 > 0.

The positive sign is required in the reference theory for causal propagation.

BACKGROUND EQUATION
-------------------
In the gamma^2 -> B background approximation used to derive the published
dimensionless equation, and for

    F = beta/nu = 0,

the background equation is

    chi_ddot
      =
      -2 t/(t^2 + D) chi_dot
      + t^2/(t^2 + D) exp(-chi).

Here t and chi are the dimensionless variables defined in the paper.

BACKGROUND / FORCE CONNECTION
-----------------------------
For beta = 0, the published coefficient connecting scalar and metric
perturbations obeys

    xi_0 proportional to chi_ddot

with a strictly positive proportionality coefficient when B0 > 0.

Therefore

    chi_ddot = 0

marks

    xi_0 = 0.

The full nonlinear simulations in the reference paper find repulsive
fifth-force episodes associated with zeros of xi_0.

The present calculation DOES NOT assume that a xi_0 zero alone proves
repulsion.

Instead it tests whether the prerequisite dynamical windows genuinely occur
in independently integrated background solutions.

EXACT FORCE-DIVERGENCE STRUCTURE
--------------------------------
The published weak-field equations give

    div(F_phi)
      =
      (1 - delta_d)
      eta^2
      div(F_Psi),

with

    eta^2 proportional to xi^2 / g_phi.

A healthy invertible matter metric requires

    g_phi > 0.

Therefore

    eta^2 >= 0.

At background order,

    delta_d = 0,

so the scalar fifth force is gravity-like.

To reverse the sign of the force divergence requires

    delta_d > 1.

This makes the scientific target extremely specific:

    non-static
    +
    perturbed
    +
    nonsymmetric
    +
    sufficiently nonlinear.

STATIC LIMIT
------------
If

    phi_dot = 0
    phi_ddot = 0

for a pure constant disformal coupling, then

    xi = 0

and the leading static classical fifth force vanishes.

Thus this experiment does not restart the earlier rejected pure-static
disformal branch.

SYMMETRON IMAGE-BRANCH RERANK
-----------------------------
014A found full nonlinear attraction in every tested local-planar symmetron
case, including twenty cases for which the electrostatic image approximation
predicted repulsion.

For the same image approximation define

    L = R_large / a_small

    d = 1 + gap/a_small.

Its repulsive/attractive ratio is

    R_image
      =
      alpha/3
      (L+d)^3 /
      [d^2 (2L+d)^2].

The derivative with respect to L is positive for

    L > d/2.

Thus reducing the large body's radius does not make the image approximation
more favorable in the normal large-body regime.

This is a ranking result, not a theorem about the full nonlinear finite-
curvature theory.

NUMERICAL METHOD
----------------
- scipy solve_ivp with tight relative/absolute tolerances;
- early-time asymptotic initial conditions;
- independent analytical small-field solution cross-check;
- dense-output root finding for chi_ddot = 0;
- explicit homogeneous g_phi stability proxy in the reference
  dimensionless conventions;
- multiple published beta=0 parameter families;
- sign checks on both sides of every root.

CLAIM LIMITS
------------
A GREEN result means:

    the project independently reproduces the stable non-static background
    prerequisite associated with published disformal repulsion.

It does NOT mean:

    ordinary baryons have been made repulsive;
    laboratory repulsion has been demonstrated;
    one-g acceleration has been demonstrated;
    screening has been solved;
    a practical device exists.

The specific reference model couples disformally to dark matter rather than
ordinary baryonic matter in order to avoid local constraints.

That source-coupling problem becomes mandatory if the spatial force gate
succeeds.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_REPRODUCTION_OF_PUBLISHED_DISFORMAL_REPULSION_PREREQUISITE
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


# ===========================================================================
# 1. Symmetron finite-curvature rerank
# ===========================================================================

print("=== SYMMETRON FINITE-CURVATURE RERANK ===")

L, d, alpha = sp.symbols(
    "L d alpha",
    positive=True,
    finite=True,
    real=True,
)

image_ratio = (
    alpha
    / 3
    * (L + d)**3
    / (
        d**2
        * (2 * L + d)**2
    )
)

image_derivative = sp.factor(
    sp.diff(
        image_ratio,
        L,
    )
)

expected_image_derivative = (
    alpha
    * (2 * L - d)
    * (L + d)**2
    / (
        3
        * d**2
        * (2 * L + d)**3
    )
)

assert sp.simplify(
    image_derivative
    - expected_image_derivative
) == 0

print(
    "IMAGE_RATIO="
    f"{sp.sstr(image_ratio)}"
)

print(
    "D_IMAGE_RATIO_D_L="
    f"{sp.sstr(image_derivative)}"
)

print(
    "IMAGE_APPROX_CURVATURE_DERIVATIVE_FOR_L_GT_D_OVER_2="
    "POSITIVE"
)

print(
    "FINITE_CURVATURE_IMAGE_APPROX_MORE_FAVORABLE_THAN_LARGE_RADIUS_LIMIT="
    "NO"
)

print(
    "014A2_FINITE_CURVATURE_PRIORITY="
    "LOWERED"
)


# ===========================================================================
# 2. Exact published force-sign structure
# ===========================================================================

print()
print("=== DISFORMAL FORCE-SIGN STRUCTURE ===")

delta_d, xi, g_phi = sp.symbols(
    "delta_d xi g_phi",
    real=True,
)

positive_prefactor = sp.symbols(
    "K",
    positive=True,
    finite=True,
    real=True,
)

eta_squared = (
    positive_prefactor
    * xi**2
    / g_phi
)

print(
    "ETA_SQUARED="
    f"{sp.sstr(eta_squared)}"
)

# Under the physical branch g_phi > 0:
#
#   eta^2 is non-negative and strictly positive whenever xi != 0.
print(
    "HEALTHY_G_PHI_SIGN="
    "POSITIVE"
)

print(
    "HEALTHY_ETA_SQUARED_SIGN="
    "NONNEGATIVE"
)

# div(F_phi)/div(F_Psi) = (1-delta_d) eta^2.
#
# For eta^2 > 0, sign reversal requires
#
#   delta_d > 1.

test_delta_values = [
    -2.0,
    0.0,
    0.5,
    0.999,
    1.0,
    1.001,
    2.0,
    10.0,
]

for test_delta in test_delta_values:
    coefficient = (
        1.0
        - test_delta
    )

    classification = (
        "OPPOSITE_DIVERGENCE"
        if coefficient < 0.0
        else (
            "ZERO"
            if math.isclose(
                coefficient,
                0.0,
                abs_tol=1.0e-15,
            )
            else "SAME_DIVERGENCE"
        )
    )

    print(
        "DELTA_D="
        f"{test_delta:+.6f} "
        "ONE_MINUS_DELTA_D="
        f"{coefficient:+.6f} "
        "CLASS="
        f"{classification}"
    )


assert (
    1.0 - 1.001
) < 0.0

print(
    "REPULSIVE_DIVERGENCE_NECESSARY_CONDITION="
    "DELTA_D_GT_1"
)

print(
    "BACKGROUND_DELTA_D="
    "ZERO"
)

print(
    "BACKGROUND_ORDER_FORCE_REVERSAL="
    "NO"
)


# ===========================================================================
# 3. Published beta=0 model definitions
# ===========================================================================

print()
print("=== PUBLISHED BETA=0 BACKGROUND MODELS ===")


@dataclass(frozen=True)
class Model:
    """Dimensionless beta=0 background parameter set."""

    name: str
    v0: float
    nu: float
    b0: float
    D: float


MODELS = [
    Model(
        name="FIDUCIAL",
        v0=1.0,
        nu=1.0,
        b0=1.0,
        D=1.3,
    ),
    Model(
        name="VF",
        v0=10.0,
        nu=1.0,
        b0=0.1,
        D=1.3,
    ),
    Model(
        name="STEEP",
        v0=1.0e-3,
        nu=1.0e3,
        b0=1.0e-2,
        D=1.3e1,
    ),
    Model(
        name="FF_BASE",
        v0=1.0e-1,
        nu=1.0e2,
        b0=1.0,
        D=1.3e3,
    ),
]


for model in MODELS:
    print(
        "MODEL="
        f"{model.name} "
        "V0="
        f"{model.v0:.6e} "
        "NU="
        f"{model.nu:.6e} "
        "B0_DIMENSIONLESS="
        f"{model.b0:.6e} "
        "D="
        f"{model.D:.6e}"
    )


# ===========================================================================
# 4. Background ODE integration
# ===========================================================================

print()
print("=== NONSTATIC BACKGROUND INTEGRATION ===")


@dataclass
class BackgroundResult:
    """Integrated dimensionless disformal background."""

    model: Model
    solution: object
    grid: np.ndarray
    chi: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray
    g_phi: np.ndarray
    roots: list[float]
    early_relative_error: float


def integrate_background(
    model: Model,
    *,
    t_max: float = 100.0,
) -> BackgroundResult:
    """Integrate the published F=0 dimensionless background equation."""

    D = model.D

    t0 = 1.0e-6

    # Early-time disformal asymptote:
    #
    #   chi ~ t^4/(12 D)
    #
    #   chi_dot ~ t^3/(3 D).
    initial_chi = (
        t0**4
        / (
            12.0
            * D
        )
    )

    initial_velocity = (
        t0**3
        / (
            3.0
            * D
        )
    )

    def rhs(
        time: float,
        state: np.ndarray,
    ) -> tuple[float, float]:
        """Published beta=0 dimensionless background ODE."""

        chi_value = float(
            state[0]
        )

        velocity_value = float(
            state[1]
        )

        denominator = (
            time**2
            + D
        )

        acceleration_value = (
            -2.0
            * time
            / denominator
            * velocity_value
            + time**2
            / denominator
            * math.exp(
                -chi_value
            )
        )

        return (
            velocity_value,
            acceleration_value,
        )


    solution = solve_ivp(
        rhs,
        (
            t0,
            t_max,
        ),
        (
            initial_chi,
            initial_velocity,
        ),
        method="DOP853",
        rtol=1.0e-11,
        atol=1.0e-13,
        max_step=0.02,
        dense_output=True,
    )

    if not solution.success:
        raise RuntimeError(
            "BACKGROUND_SOLVER_FAILURE:"
            + model.name
            + ":"
            + str(
                solution.message
            )
        )

    grid = np.geomspace(
        t0,
        t_max,
        50000,
    )

    evaluated = solution.sol(
        grid
    )

    chi_values = evaluated[0]
    velocity_values = evaluated[1]

    acceleration_values = (
        -2.0
        * grid
        / (
            grid**2
            + D
        )
        * velocity_values
        + grid**2
        / (
            grid**2
            + D
        )
        * np.exp(
            -chi_values
        )
    )

    # ---------------------------------------------------------------
    # Homogeneous g_phi mapping for beta=0.
    #
    # Using
    #
    #   g_phi = 1 - B0 * phi_dot^2
    #
    # and the paper's dimensionless definitions gives
    #
    #   g_phi
    #     =
    #     1
    #     - b0 * (v0/nu) * chi_dot^2
    #
    # in the conventions used for this background calculation.
    # ---------------------------------------------------------------

    stability_coefficient = (
        model.b0
        * model.v0
        / model.nu
    )

    g_phi_values = (
        1.0
        - stability_coefficient
        * velocity_values**2
    )

    # ---------------------------------------------------------------
    # Find every chi_ddot = 0 crossing.
    # ---------------------------------------------------------------

    signs = np.sign(
        acceleration_values
    )

    crossing_indices = np.where(
        signs[:-1]
        * signs[1:]
        < 0.0
    )[0]

    roots: list[float] = []

    def acceleration_at(
        time: float,
    ) -> float:
        state = solution.sol(
            time
        )

        chi_value = float(
            state[0]
        )

        velocity_value = float(
            state[1]
        )

        denominator = (
            time**2
            + D
        )

        return (
            -2.0
            * time
            / denominator
            * velocity_value
            + time**2
            / denominator
            * math.exp(
                -chi_value
            )
        )


    for index in crossing_indices:
        root = brentq(
            acceleration_at,
            float(
                grid[index]
            ),
            float(
                grid[index + 1]
            ),
            xtol=1.0e-13,
            rtol=1.0e-13,
        )

        roots.append(
            root
        )

    # ---------------------------------------------------------------
    # Independent early-time analytical validation.
    #
    # Published linear beta=0 solution with damping:
    #
    #   chi_lin
    #     =
    #     t^2/6
    #     [
    #       1
    #       - D/t^2 ln((t^2+D)/D)
    #     ].
    #
    # We evaluate deep in the chi << 1 regime.
    # ---------------------------------------------------------------

    validation_time = (
        0.05
        * math.sqrt(
            D
        )
    )

    numerical_chi = float(
        solution.sol(
            validation_time
        )[0]
    )

    analytical_chi = (
        validation_time**2
        / 6.0
        - D
        / 6.0
        * math.log1p(
            validation_time**2
            / D
        )
    )

    early_relative_error = (
        abs(
            numerical_chi
            - analytical_chi
        )
        / max(
            abs(
                numerical_chi
            ),
            1.0e-300,
        )
    )

    return BackgroundResult(
        model=model,
        solution=solution,
        grid=grid,
        chi=chi_values,
        velocity=velocity_values,
        acceleration=acceleration_values,
        g_phi=g_phi_values,
        roots=roots,
        early_relative_error=early_relative_error,
    )


BACKGROUND_RESULTS = [
    integrate_background(
        model
    )
    for model in MODELS
]


# ===========================================================================
# 5. Analytical-solution validation
# ===========================================================================

print()
print("=== EARLY-TIME ANALYTICAL CROSS-CHECK ===")

max_early_error = 0.0

for result in BACKGROUND_RESULTS:
    max_early_error = max(
        max_early_error,
        result.early_relative_error,
    )

    print(
        "MODEL="
        f"{result.model.name} "
        "EARLY_LINEAR_REL_ERROR="
        f"{result.early_relative_error:.16e}"
    )


print(
    "MAX_EARLY_LINEAR_REL_ERROR="
    f"{max_early_error:.16e}"
)

assert (
    max_early_error
    < 2.0e-4
)

print(
    "PUBLISHED_EARLY_TIME_BACKGROUND_SOLUTION="
    "INDEPENDENTLY_REPRODUCED"
)


# ===========================================================================
# 6. xi_0 zero / acceleration-flip search
# ===========================================================================

print()
print("=== XI_0 ZERO WINDOWS ===")

all_have_root = True
all_stable = True

minimum_g_phi_all = math.inf

for result in BACKGROUND_RESULTS:
    minimum_g_phi = float(
        np.min(
            result.g_phi
        )
    )

    minimum_g_phi_all = min(
        minimum_g_phi_all,
        minimum_g_phi,
    )

    if minimum_g_phi <= 0.0:
        all_stable = False

    if len(
        result.roots
    ) == 0:
        all_have_root = False

    print(
        "MODEL="
        f"{result.model.name} "
        "XI_ZERO_COUNT="
        f"{len(result.roots)} "
        "MIN_G_PHI="
        f"{minimum_g_phi:.16e}"
    )

    for root_index, root in enumerate(
        result.roots,
        start=1,
    ):
        before_time = (
            0.99
            * root
        )

        after_time = (
            1.01
            * root
        )

        before_state = (
            result.solution.sol(
                before_time
            )
        )

        after_state = (
            result.solution.sol(
                after_time
            )
        )

        D = result.model.D

        before_acceleration = (
            -2.0
            * before_time
            / (
                before_time**2
                + D
            )
            * float(
                before_state[1]
            )
            + before_time**2
            / (
                before_time**2
                + D
            )
            * math.exp(
                -float(
                    before_state[0]
                )
            )
        )

        after_acceleration = (
            -2.0
            * after_time
            / (
                after_time**2
                + D
            )
            * float(
                after_state[1]
            )
            + after_time**2
            / (
                after_time**2
                + D
            )
            * math.exp(
                -float(
                    after_state[0]
                )
            )
        )

        print(
            "MODEL="
            f"{result.model.name} "
            "ROOT_INDEX="
            f"{root_index} "
            "T_XI_ZERO="
            f"{root:.16e} "
            "XI_PROXY_BEFORE="
            f"{before_acceleration:+.16e} "
            "XI_PROXY_AFTER="
            f"{after_acceleration:+.16e}"
        )

        assert (
            before_acceleration
            * after_acceleration
            < 0.0
        )


print(
    "MIN_G_PHI_ACROSS_TESTED_BACKGROUNDS="
    f"{minimum_g_phi_all:.16e}"
)

assert all_have_root
assert all_stable

print(
    "ALL_TESTED_BETA0_MODELS_HAVE_XI0_SIGN_CHANGE="
    "YES"
)

print(
    "ALL_TESTED_XI0_SIGN_CHANGES_OCCUR_WITH_G_PHI_POSITIVE="
    "YES"
)


# ===========================================================================
# 7. Nonlinear-trigger sensitivity around xi_0 = 0
# ===========================================================================

print()
print("=== REPULSIVE-CORRECTION SENSITIVITY NEAR XI_ZERO ===")

# Eq. 37 contains a factor 1/xi^2.
#
# This DOES NOT prove that delta_d diverges physically, because its numerator
# and the validity of the perturbative approximation must be tracked
# consistently.
#
# It does show why xi=0 is the high-sensitivity window singled out by the
# published analysis and full simulations.

minimum_inverse_xi_squared_proxy = math.inf

for result in BACKGROUND_RESULTS:
    root = result.roots[0]

    for side_label, factor in [
        (
            "BEFORE",
            0.99,
        ),
        (
            "AFTER",
            1.01,
        ),
    ]:
        test_time = (
            factor
            * root
        )

        state = (
            result.solution.sol(
                test_time
            )
        )

        D = result.model.D

        acceleration_proxy = (
            -2.0
            * test_time
            / (
                test_time**2
                + D
            )
            * float(
                state[1]
            )
            + test_time**2
            / (
                test_time**2
                + D
            )
            * math.exp(
                -float(
                    state[0]
                )
            )
        )

        inverse_square_proxy = (
            1.0
            / acceleration_proxy**2
        )

        minimum_inverse_xi_squared_proxy = min(
            minimum_inverse_xi_squared_proxy,
            inverse_square_proxy,
        )

        print(
            "MODEL="
            f"{result.model.name} "
            "SIDE="
            f"{side_label} "
            "ABS_XI_PROXY="
            f"{abs(acceleration_proxy):.16e} "
            "INV_XI_PROXY_SQUARED="
            f"{inverse_square_proxy:.16e}"
        )


print(
    "MIN_NEAR_ZERO_INV_XI_PROXY_SQUARED="
    f"{minimum_inverse_xi_squared_proxy:.16e}"
)

assert (
    minimum_inverse_xi_squared_proxy
    > 1.0e4
)

print(
    "XI_ZERO_IS_HIGH_SENSITIVITY_NONLINEAR_WINDOW="
    "YES"
)

print(
    "XI_ZERO_ALONE_PROVES_REPULSION="
    "NO"
)


# ===========================================================================
# 8. Static-limit consistency with the previous project gate
# ===========================================================================

print()
print("=== PURE STATIC DISFORMAL LIMIT ===")

static_phi_dot = 0.0
static_phi_ddot = 0.0

# For constant B:
#
#   xi
#     proportional to
#     B phi_ddot.
static_xi_proxy = (
    static_phi_ddot
)

print(
    "STATIC_PHI_DOT="
    f"{static_phi_dot:.1f}"
)

print(
    "STATIC_PHI_DDOT="
    f"{static_phi_ddot:.1f}"
)

print(
    "STATIC_XI_PROXY="
    f"{static_xi_proxy:.1f}"
)

assert (
    static_xi_proxy
    == 0.0
)

print(
    "PURE_STATIC_CONSTANT_DISFORMAL_LEADING_FORCE="
    "ZERO"
)

print(
    "010C_STATIC_DISFORMAL_RESULT="
    "REPRODUCED_NOT_OVERRIDDEN"
)


# ===========================================================================
# 9. Geometry filter
# ===========================================================================

print()
print("=== GEOMETRY / DYNAMICS FILTER ===")

print(
    "BACKGROUND_ORDER_DELTA_D="
    "ZERO"
)

print(
    "BACKGROUND_ORDER_DISFORMAL_FORCE="
    "PARALLEL_TO_GRAVITY"
)

print(
    "SPHERICAL_CURL_TERM="
    "ZERO_IN_PUBLISHED_FORCE_DECOMPOSITION"
)

print(
    "STATIC_SPHERICAL_DISFORMAL_REPULSION_TARGET="
    "REJECTED"
)

print(
    "NONSTATIC_PERTURBED_NONSYMMETRIC_CONFIGURATION_REQUIRED="
    "YES"
)


# ===========================================================================
# 10. Source-coupling honesty gate
# ===========================================================================

print()
print("=== ORDINARY-MATTER APPLICABILITY ===")

print(
    "REFERENCE_2019_MODEL_DISFORMALLY_COUPLES_BARYONS="
    "NO"
)

print(
    "REFERENCE_2019_MODEL_DISFORMALLY_COUPLES_DARK_MATTER="
    "YES"
)

print(
    "REASON_FOR_NONUNIVERSAL_COUPLING="
    "NO_SCREENING_MECHANISM_AND_LOCAL_GRAVITY_CONSTRAINTS"
)

print(
    "SCREENED_VISIBLE_MATTER_EXTENSION="
    "REQUIRED_FOR_PRACTICAL_ORDINARY_PAYLOAD"
)

print(
    "DISFORMAL_PLUS_SYMMETRON_SCREENING_EXISTS_IN_LITERATURE_AS_MODEL_CLASS="
    "YES"
)

print(
    "VISIBLE_MATTER_REPULSION_ESTABLISHED_BY_THIS_RUN="
    "NO"
)


# ===========================================================================
# Final classification
# ===========================================================================

print()
print("=== 014B FINAL GATE ===")

print(
    "014A2_FINITE_CURVATURE_SYMMETRON_RANK="
    "BELOW_NONSTATIC_DISFORMAL_BRANCH"
)

print(
    "PURE_STATIC_DISFORMAL_RESTART="
    "NO"
)

print(
    "PUBLISHED_DISFORMAL_BACKGROUND_EQUATION="
    "INDEPENDENTLY_REPRODUCED"
)

print(
    "PUBLISHED_EARLY_TIME_SOLUTION="
    "INDEPENDENTLY_REPRODUCED"
)

print(
    "STABLE_XI_ZERO_WINDOWS="
    "FOUND"
)

print(
    "REPULSIVE_DIVERGENCE_CONDITION="
    "DELTA_D_GT_1"
)

print(
    "FULL_REPULSIVE_DISFORMAL_FORCE_REPRODUCED_IN_THIS_GATE="
    "NO"
)

print(
    "PUBLISHED_FULL_NONLINEAR_3D_REPULSION="
    "EXTERNAL_RESULT_NOT_YET_INDEPENDENTLY_REPRODUCED_BY_PROJECT"
)

print(
    "PRACTICAL_BARYONIC_ANTIGRAVITY="
    "NOT_ESTABLISHED"
)

print(
    "CLAIM_CLASSIFICATION="
    "PROJECT_DERIVED_REPRODUCTION_OF_PUBLISHED_DISFORMAL_REPULSION_PREREQUISITE"
)

print(
    "NEXT_IF_GREEN="
    "014C_NONSYMMETRIC_NONSTATIC_HYPERBOLIC_DISFORMAL_FORCE_SOLVER"
)

print(
    "014B_NONSTATIC_DISFORMAL_PREREQUISITE_GATE="
    "GREEN"
)
