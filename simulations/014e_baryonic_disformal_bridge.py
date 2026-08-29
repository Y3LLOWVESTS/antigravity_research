"""014E — baryonic disformal bridge feasibility gate.

PURPOSE
-------
Determine whether the local total-force reversal reproduced in 014D can be
transferred from its reduced dark-sector disformal model to ordinary
Standard-Model matter using the simplest physically motivated bridges.

014D established:

    PROJECT_REPRODUCED_LOCAL_TOTAL_FORCE_REVERSAL
        =
        YES_IN_CONTROLLED_REDUCED_DISFORMAL_MODEL

with:

    first coarse reversal:
        b0 = 0.24

    fully validated candidate:
        b0 = 0.28

and with the disformal metric remaining nondegenerate.

The outstanding problem is no longer the sign of the force.

The outstanding problem is whether a coupling strong enough to produce that
effect can consistently act on ordinary matter.

SCIENTIFIC QUESTION
-------------------
Can the dimensionless disformal strength required by 014D be reconciled with
a Standard-Model disformal coupling using:

1. a constant universal disformal coefficient;
2. ordinary symmetron conformal screening;
3. a collider-safe constant coefficient compensated by a larger scalar
   time derivative;
4. or a moderately environment-dependent disformal coefficient?

The gate deliberately does NOT build another large PDE solver.

The purpose is to test physical realizability before spending more numerical
compute.

PUBLISHED DISFORMAL NORMALIZATION
---------------------------------
Llinares, Hagala & Mota define

    b0 = H0^2 M_Pl^2 B0.

Thus b0 is dimensionless.

014D's variable called B0 was numerically this dimensionless b0 because the
reduced calculation used

    H0 = M_Pl = 1.

This notation distinction is critical.

For a minimal constant disformal Standard-Model operator,

    B0 = 1 / M_D^4,

where M_D is the disformal suppression scale.

Therefore

    b0
      =
      H0^2 M_Pl^2 / M_D^4,

and

    M_D
      =
      sqrt(H0 M_Pl) b0^(-1/4).

STANDARD-MODEL COLLIDER INPUT
-----------------------------
Brax, Burrage & Englert (Phys. Rev. D 92, 044036, 2015) considered the
constant universal operator

    L_int
      =
      (1/M_D^4)
      partial_mu(phi)
      partial_nu(phi)
      T^(mu nu)

and obtained an LHC Run-1 monojet constraint of approximately

    M_D >= 650 GeV.

This is the primary empirical input for this gate because it matches the
minimal constant disformal operator directly.

A later ATLAS dark-energy EFT search excludes a related Horndeski suppression
scale below approximately 1.5 TeV.

That result is NOT treated as the same operator or normalization here and is
therefore only contextual; it is not used in any rejection assertion.

SYMMETRON SCREENING INPUT
-------------------------
Conventional symmetron screening suppresses the leading conformal coupling
because that coupling is proportional to the local symmetron vacuum
expectation value.

A recent explicit symmetron analysis including disformal interactions shows
that the minimal constant disformal derivative operator does not acquire this
additional VEV suppression.

Therefore:

    conformal symmetron screening alone

does not automatically hide

    constant B * partial(phi)^2 * T.

This statement does NOT prove that every possible disformal screening
mechanism fails.

KINETIC-COMPENSATION TEST
-------------------------
For a homogeneous background,

    g_phi
      =
      1 - B0 phi_dot^2.

Define

    q
      =
      B0 phi_dot^2
      =
      1 - g_phi.

At the first 014D reversal threshold b0=0.24, the homogeneous background had

    g_phi ~= 0.2573528613,

so

    q ~= 0.7426471387.

If collider constraints force

    B0 <= 1/(650 GeV)^4

but one attempts to reproduce the same dimensionless deformation q by
increasing phi_dot, then

    phi_dot^2
      =
      q M_D^4.

For a canonical scalar, the time-kinetic energy density alone is

    K
      =
      phi_dot^2 / 2
      =
      q M_D^4 / 2.

The gate converts this into SI units and asks whether a macroscopic weak-field
laboratory region could contain this energy density.

This is NOT a theorem against every noncanonical theory.

It is a realizability test of the canonical continuation of the mechanism
actually simulated.

ENVIRONMENT-DEPENDENT ESCAPE
----------------------------
A field-dependent coefficient remains logically possible.

For example,

    B(phi)
      =
      B_dense exp[
          beta (phi-phi_dense)/M_Pl
      ].

To suppress the interaction in collider/dense conditions while retaining the
014D strength in the operating region requires

    B_operating / B_dense
        >=
        required hierarchy.

Equivalently,

    Delta ln B
        >=
        ln(required hierarchy).

For the exponential model,

    |beta Delta phi / M_Pl|
        >=
        Delta ln B.

This gate computes that required exponent.

A very large required hierarchy does not mathematically exclude such a
function.

It tells us that this would be a genuinely new model-building problem, not a
minor modification of the constant-B theory.

CLAIM LIMITS
------------
This gate does NOT prove:

- all baryonic disformal theories impossible;
- all environment-dependent B(phi) models impossible;
- all UV completions impossible;
- all noncanonical scalar theories impossible;
- global antigravity impossible.

It tests the minimal and most direct bridge from the project-reproduced 014D
mechanism to ordinary matter.

The positive 014D force-reversal result is preserved regardless of the
outcome of this gate.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_BARYONIC_DISFORMAL_BRIDGE_FEASIBILITY_BOUND
"""

from __future__ import annotations

import math

import sympy as sp


# ===========================================================================
# 1. Inputs and constants
# ===========================================================================

print("=== INPUTS AND NOTATION ===")

# Published cosmology used in the disformal reference work.
H0_KM_S_MPC = 67.74

# SI / natural-unit constants.
MPC_M = 3.0856775814913673e22
HBAR_EV_S = 6.582119569e-16
HBARC_EV_M = 1.973269804e-7
EV_J = 1.602176634e-19

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11

# Reduced Planck mass:
#
#     M_Pl = 1/sqrt(8 pi G)
#
# in natural particle-physics energy units.
MPL_REDUCED_EV = 2.435e27

# 014D project-derived inputs.
FIRST_REVERSAL_b0 = 0.24
VALIDATED_REVERSAL_b0 = 0.28

FIRST_REVERSAL_BACKGROUND_GPHI = (
    2.5735286127569845e-1
)

VALIDATED_REVERSAL_MIN_GPHI = (
    1.3850683595823443e-1
)

# Primary directly matching constant-disformal collider constraint.
CMS_RUN1_CONSTANT_DISFORMAL_BOUND_GEV = 650.0

# Related later ATLAS dark-energy EFT result.
#
# IMPORTANT:
# This is a related Horndeski L2 suppression scale and is NOT used as though
# it were an identical normalization to the constant disformal operator.
ATLAS_RELATED_HORNDESKI_M2_GEV = 1486.0


print(
    "014D_CODE_COUPLING_INTERPRETATION="
    "DIMENSIONLESS_b0_NOT_DIMENSIONFUL_B0"
)

print(
    "FIRST_REVERSAL_b0="
    f"{FIRST_REVERSAL_b0:.16e}"
)

print(
    "VALIDATED_REVERSAL_b0="
    f"{VALIDATED_REVERSAL_b0:.16e}"
)

print(
    "FIRST_REVERSAL_BACKGROUND_GPHI="
    f"{FIRST_REVERSAL_BACKGROUND_GPHI:.16e}"
)

print(
    "CMS_RUN1_CONSTANT_DISFORMAL_BOUND_GEV="
    f"{CMS_RUN1_CONSTANT_DISFORMAL_BOUND_GEV:.16e}"
)

print(
    "ATLAS_RELATED_HORNDESKI_M2_GEV="
    f"{ATLAS_RELATED_HORNDESKI_M2_GEV:.16e}"
)

print(
    "ATLAS_RELATED_OPERATOR_USED_AS_PRIMARY_BOUND="
    "NO"
)


# ===========================================================================
# 2. Exact symbolic normalization map
# ===========================================================================

print()
print("=== EXACT DIMENSIONLESS-TO-PHYSICAL MAP ===")

H, P, M, b = sp.symbols(
    "H P M b",
    positive=True,
    finite=True,
    real=True,
)

b_expression = (
    H**2
    * P**2
    / M**4
)

M_solution = (
    sp.sqrt(
        H * P
    )
    * b**(
        -sp.Rational(
            1,
            4,
        )
    )
)

symbolic_residual = sp.simplify(
    b_expression.subs(
        M,
        M_solution,
    )
    - b
)

print(
    "b0_FORMULA="
    "H0_SQUARED_MPL_SQUARED_OVER_MD_FOURTH"
)

print(
    "MD_FORMULA="
    "SQRT_H0_MPL_TIMES_b0_TO_MINUS_ONE_QUARTER"
)

print(
    "SYMBOLIC_MAP_RESIDUAL="
    f"{sp.sstr(symbolic_residual)}"
)

assert (
    symbolic_residual
    == 0
)

print(
    "DISFORMAL_NORMALIZATION_MAP="
    "PROVED"
)


# ===========================================================================
# 3. Convert H0 to natural energy units
# ===========================================================================

print()
print("=== COSMOLOGICAL ENERGY SCALE ===")

H0_PER_SECOND = (
    H0_KM_S_MPC
    * 1000.0
    / MPC_M
)

H0_EV = (
    H0_PER_SECOND
    * HBAR_EV_S
)

H0_MPL_EV2 = (
    H0_EV
    * MPL_REDUCED_EV
)

COSMOLOGICAL_DISFORMAL_BASE_EV = math.sqrt(
    H0_MPL_EV2
)

print(
    "H0_PER_SECOND="
    f"{H0_PER_SECOND:.16e}"
)

print(
    "H0_EV="
    f"{H0_EV:.16e}"
)

print(
    "H0_TIMES_MPL_EV2="
    f"{H0_MPL_EV2:.16e}"
)

print(
    "SQRT_H0_MPL_EV="
    f"{COSMOLOGICAL_DISFORMAL_BASE_EV:.16e}"
)

print(
    "SQRT_H0_MPL_MEV="
    f"{COSMOLOGICAL_DISFORMAL_BASE_EV*1.0e3:.16e}"
)


# ===========================================================================
# 4. Map 014D reversal strength to physical disformal scale
# ===========================================================================

print()
print("=== 014D REVERSAL PHYSICAL SCALE ===")


def disformal_scale_from_b0(
    b0: float,
) -> float:
    """Return M_D in eV for constant B=1/M_D^4."""

    return (
        COSMOLOGICAL_DISFORMAL_BASE_EV
        * b0**(-0.25)
    )


def b0_from_disformal_scale(
    scale_ev: float,
) -> float:
    """Return dimensionless b0 for constant B=1/M_D^4."""

    return (
        H0_MPL_EV2
        / scale_ev**2
    )**2


for label, value in [
    (
        "FIRST_REVERSAL",
        FIRST_REVERSAL_b0,
    ),
    (
        "VALIDATED_REVERSAL",
        VALIDATED_REVERSAL_b0,
    ),
    (
        "COARSE_B0_0P30",
        0.30,
    ),
]:
    scale_ev = disformal_scale_from_b0(
        value
    )

    round_trip = b0_from_disformal_scale(
        scale_ev
    )

    relative_error = abs(
        round_trip
        - value
    ) / value

    print(
        "CASE="
        f"{label} "
        "b0="
        f"{value:.16e} "
        "MD_EV="
        f"{scale_ev:.16e} "
        "MD_MEV="
        f"{scale_ev*1.0e3:.16e} "
        "ROUNDTRIP_REL_ERROR="
        f"{relative_error:.16e}"
    )

    assert (
        relative_error
        < 1.0e-14
    )


FIRST_REVERSAL_MD_EV = (
    disformal_scale_from_b0(
        FIRST_REVERSAL_b0
    )
)

VALIDATED_REVERSAL_MD_EV = (
    disformal_scale_from_b0(
        VALIDATED_REVERSAL_b0
    )
)

print(
    "FIRST_REVERSAL_DISFORMAL_SCALE_MEV="
    f"{FIRST_REVERSAL_MD_EV*1.0e3:.16e}"
)

print(
    "VALIDATED_REVERSAL_DISFORMAL_SCALE_MEV="
    f"{VALIDATED_REVERSAL_MD_EV*1.0e3:.16e}"
)


# ===========================================================================
# 5. Direct constant-B Standard-Model bridge
# ===========================================================================

print()
print("=== CONSTANT-B STANDARD-MODEL COLLIDER BRIDGE ===")

CMS_BOUND_EV = (
    CMS_RUN1_CONSTANT_DISFORMAL_BOUND_GEV
    * 1.0e9
)

COLLIDER_ALLOWED_b0_MAX = (
    b0_from_disformal_scale(
        CMS_BOUND_EV
    )
)

B_HIERARCHY_TO_FIRST_REVERSAL = (
    FIRST_REVERSAL_b0
    / COLLIDER_ALLOWED_b0_MAX
)

B_HIERARCHY_LOG10 = math.log10(
    B_HIERARCHY_TO_FIRST_REVERSAL
)

MD_SCALE_GAP = (
    CMS_BOUND_EV
    / FIRST_REVERSAL_MD_EV
)

MD_SCALE_GAP_LOG10 = math.log10(
    MD_SCALE_GAP
)

print(
    "COLLIDER_ALLOWED_CONSTANT_B_b0_MAX="
    f"{COLLIDER_ALLOWED_b0_MAX:.16e}"
)

print(
    "FIRST_REVERSAL_b0_OVER_COLLIDER_ALLOWED_b0="
    f"{B_HIERARCHY_TO_FIRST_REVERSAL:.16e}"
)

print(
    "COUPLING_HIERARCHY_ORDERS_OF_MAGNITUDE="
    f"{B_HIERARCHY_LOG10:.16e}"
)

print(
    "COLLIDER_MD_OVER_FIRST_REVERSAL_MD="
    f"{MD_SCALE_GAP:.16e}"
)

print(
    "DISFORMAL_SCALE_GAP_ORDERS_OF_MAGNITUDE="
    f"{MD_SCALE_GAP_LOG10:.16e}"
)

assert (
    COLLIDER_ALLOWED_b0_MAX
    < 1.0e-58
)

assert (
    B_HIERARCHY_TO_FIRST_REVERSAL
    > 1.0e57
)

assert (
    MD_SCALE_GAP
    > 1.0e14
)

print(
    "MINIMAL_UNIVERSAL_CONSTANT_B_STANDARD_MODEL_BRIDGE="
    "INCOMPATIBLE_WITH_DIRECT_CONSTANT_OPERATOR_COLLIDER_BOUND"
)


# ===========================================================================
# 6. Symmetron conformal-screening bridge
# ===========================================================================

print()
print("=== SYMMETRON SCREENING STRUCTURE ===")

# External literature facts:
#
# Conventional symmetron:
#
#     leading conformal coupling ~ phi_VEV
#
# and therefore vanishes as the local VEV goes to zero.
#
# Minimal constant disformal interaction:
#
#     (partial phi)^2 T / M_e^4
#
# receives no corresponding VEV factor when expanded around the local
# background.

print(
    "CONVENTIONAL_SYMMETRON_CONFORMAL_COUPLING="
    "VEV_DEPENDENT"
)

print(
    "DENSE_PHASE_SYMMETRON_CONFORMAL_SCREENING="
    "YES"
)

print(
    "MINIMAL_CONSTANT_DISFORMAL_OPERATOR="
    "NO_ADDITIONAL_VEV_SUPPRESSION"
)

print(
    "CONFORMAL_SYMMETRON_SCREENING_ALONE_HIDES_CONSTANT_DISFORMAL_OPERATOR="
    "NO"
)

print(
    "ALL_DISFORMAL_SCREENING_MECHANISMS_REJECTED="
    "NO"
)


# ===========================================================================
# 7. Collider-safe B with kinetic compensation
# ===========================================================================

print()
print("=== KINETIC-COMPENSATION FEASIBILITY ===")

# At the homogeneous 014D threshold:
#
#     g_phi = 1 - B phi_dot^2.
#
# Therefore:
#
#     q = B phi_dot^2 = 1-g_phi.

Q_FIRST_REVERSAL = (
    1.0
    - FIRST_REVERSAL_BACKGROUND_GPHI
)

print(
    "FIRST_REVERSAL_Q_EQUALS_B_PHIDOT2="
    f"{Q_FIRST_REVERSAL:.16e}"
)

assert (
    0.0
    < Q_FIRST_REVERSAL
    < 1.0
)

# If B=1/M_D^4 then
#
#     phi_dot^2 = q M_D^4
#
# and for a canonical scalar
#
#     K = phi_dot^2/2.

CANONICAL_KINETIC_EV4 = (
    0.5
    * Q_FIRST_REVERSAL
    * CMS_BOUND_EV**4
)

EV4_TO_J_M3 = (
    EV_J
    / HBARC_EV_M**3
)

CANONICAL_KINETIC_J_M3 = (
    CANONICAL_KINETIC_EV4
    * EV4_TO_J_M3
)

MASS_DENSITY_KG_M3 = (
    CANONICAL_KINETIC_J_M3
    / C_LIGHT**2
)

print(
    "ONE_EV4_IN_J_M3="
    f"{EV4_TO_J_M3:.16e}"
)

print(
    "MATCHED_Q_CANONICAL_KINETIC_EV4="
    f"{CANONICAL_KINETIC_EV4:.16e}"
)

print(
    "MATCHED_Q_CANONICAL_KINETIC_J_M3="
    f"{CANONICAL_KINETIC_J_M3:.16e}"
)

print(
    "MATCHED_Q_MASS_EQUIVALENT_DENSITY_KG_M3="
    f"{MASS_DENSITY_KG_M3:.16e}"
)

assert (
    CANONICAL_KINETIC_J_M3
    > 1.0e48
)


# ===========================================================================
# 8. Weak-field compactness audit of that energy density
# ===========================================================================

print()
print("=== KINETIC-ENERGY COMPACTNESS AUDIT ===")

# Uniform spherical region containing energy density u:
#
#     M = (4 pi/3) R^3 u/c^2
#
# hence
#
#     2GM/(R c^2)
#       =
#       8 pi G u R^2/(3 c^4).
#
# The compactness-one radius is
#
#     Rcrit
#       =
#       sqrt[
#           3 c^4/(8 pi G u)
#       ].

R_CRIT_M = math.sqrt(
    3.0
    * C_LIGHT**4
    / (
        8.0
        * math.pi
        * G_NEWTON
        * CANONICAL_KINETIC_J_M3
    )
)

print(
    "COMPACTNESS_ONE_RADIUS_M="
    f"{R_CRIT_M:.16e}"
)

print(
    "COMPACTNESS_ONE_RADIUS_MM="
    f"{R_CRIT_M*1.0e3:.16e}"
)


def compactness(
    radius_m: float,
) -> float:
    """Return 2GM/(Rc^2) for uniform kinetic-energy density."""

    return (
        8.0
        * math.pi
        * G_NEWTON
        * CANONICAL_KINETIC_J_M3
        * radius_m**2
        / (
            3.0
            * C_LIGHT**4
        )
    )


for radius_m in [
    1.0,
    0.10,
    0.01,
    0.001,
]:
    value = compactness(
        radius_m
    )

    print(
        "RADIUS_M="
        f"{radius_m:.6e} "
        "TWO_GM_OVER_R_C2="
        f"{value:.16e}"
    )


assert (
    compactness(
        1.0
    )
    > 1.0e4
)

assert (
    compactness(
        0.01
    )
    > 1.0
)

assert (
    R_CRIT_M
    < 0.004
)

print(
    "MATCHED_014D_Q_WITH_COLLIDER_SAFE_CONSTANT_B_MACROSCOPIC_WEAK_FIELD="
    "NO_FOR_CANONICAL_UNIFORM_ENERGY_REALIZATION"
)


# ===========================================================================
# 9. Environment-dependent B(phi) escape requirement
# ===========================================================================

print()
print("=== ENVIRONMENT-DEPENDENT B REQUIREMENT ===")

# To have collider/dense B <= B_allowed while retaining operating-region
# B >= B_required, the minimum required ratio is exactly the b0 ratio since
# H0 and M_Pl cancel.

MIN_B_OPERATING_OVER_B_DENSE = (
    B_HIERARCHY_TO_FIRST_REVERSAL
)

MIN_DELTA_LN_B = math.log(
    MIN_B_OPERATING_OVER_B_DENSE
)

print(
    "MIN_B_OPERATING_OVER_B_DENSE="
    f"{MIN_B_OPERATING_OVER_B_DENSE:.16e}"
)

print(
    "MIN_DELTA_LOG10_B="
    f"{math.log10(MIN_B_OPERATING_OVER_B_DENSE):.16e}"
)

print(
    "MIN_DELTA_LN_B="
    f"{MIN_DELTA_LN_B:.16e}"
)

assert (
    MIN_DELTA_LN_B
    > 130.0
)

# For
#
#     B(phi) = B_dense exp(beta Delta_phi/M_Pl)
#
# the required invariant exponent is
#
#     |beta Delta_phi/M_Pl| >= Delta ln B.

for delta_phi_over_mpl in [
    0.1,
    1.0,
    10.0,
    100.0,
]:
    beta_required = (
        MIN_DELTA_LN_B
        / delta_phi_over_mpl
    )

    print(
        "ASSUMED_ABS_DELTA_PHI_OVER_MPL="
        f"{delta_phi_over_mpl:.6e} "
        "MIN_ABS_BETA="
        f"{beta_required:.16e}"
    )


print(
    "EXPONENTIAL_B_INVARIANT_REQUIREMENT="
    "ABS_BETA_DELTA_PHI_OVER_MPL_GE_MIN_DELTA_LN_B"
)

print(
    "ENVIRONMENT_DEPENDENT_B_ESCAPE="
    "LOGICALLY_OPEN"
)

print(
    "ENVIRONMENT_DEPENDENT_B_ESCAPE_IS_MINOR_PARAMETER_TWEAK="
    "NO"
)


# ===========================================================================
# 10. Related modern collider cross-check
# ===========================================================================

print()
print("=== RELATED MODERN COLLIDER CONTEXT ===")

print(
    "ATLAS_2021_RELATED_DARK_ENERGY_EFT_M2_BOUND_GEV="
    f"{ATLAS_RELATED_HORNDESKI_M2_GEV:.16e}"
)

print(
    "ATLAS_2021_OPERATOR_IDENTICAL_TO_CONSTANT_DISFORMAL_OPERATOR="
    "NO"
)

print(
    "ATLAS_2021_BOUND_USED_TO_DERIVE_PRIMARY_014E_REJECTION="
    "NO"
)

print(
    "RELATED_MODERN_COLLIDER_CONSTRAINT_DIRECTION="
    "STRENGTHENS_NOT_WEAKENS_STANDARD_MODEL_COUPLING_TENSION"
)


# ===========================================================================
# 11. Decision matrix
# ===========================================================================

print()
print("=== BARYONIC BRIDGE DECISION MATRIX ===")

constant_b_bridge_survives = (
    COLLIDER_ALLOWED_b0_MAX
    >= FIRST_REVERSAL_b0
)

canonical_compensation_macroscopic_survives = (
    compactness(
        1.0
    )
    < 0.1
)

conformal_symmetron_alone_screens_constant_b = (
    False
)

print(
    "DIRECT_CONSTANT_B_BRIDGE_SURVIVES="
    + (
        "YES"
        if constant_b_bridge_survives
        else "NO"
    )
)

print(
    "CONFORMAL_SYMMETRON_VEV_SCREENING_ALONE_SURVIVES="
    + (
        "YES"
        if conformal_symmetron_alone_screens_constant_b
        else "NO"
    )
)

print(
    "CANONICAL_KINETIC_COMPENSATION_AT_1M_WEAK_FIELD_SURVIVES="
    + (
        "YES"
        if canonical_compensation_macroscopic_survives
        else "NO"
    )
)

print(
    "FIELD_DEPENDENT_OR_UV_COMPLETED_DISFORMAL_BRIDGE="
    "NOT_EXCLUDED"
)

assert not (
    constant_b_bridge_survives
)

assert not (
    conformal_symmetron_alone_screens_constant_b
)

assert not (
    canonical_compensation_macroscopic_survives
)


# ===========================================================================
# 12. Final classification
# ===========================================================================

print()
print("=== 014E FINAL GATE ===")

print(
    "014D_LOCAL_TOTAL_FORCE_REVERSAL_RESULT="
    "PRESERVED"
)

print(
    "014D_REPULSIVE_SIGN_OR_TOTAL_REVERSAL_RETRACTED="
    "NO"
)

print(
    "FIRST_014D_REVERSAL_PHYSICAL_CONSTANT_B_SCALE="
    f"{FIRST_REVERSAL_MD_EV*1.0e3:.16e}"
    "_MEV"
)

print(
    "DIRECT_STANDARD_MODEL_CONSTANT_B_SCALE_BOUND="
    f"{CMS_RUN1_CONSTANT_DISFORMAL_BOUND_GEV:.16e}"
    "_GEV"
)

print(
    "CONSTANT_B_COUPLING_GAP_TO_FIRST_REVERSAL="
    f"{B_HIERARCHY_TO_FIRST_REVERSAL:.16e}"
)

print(
    "MINIMAL_CONSTANT_B_BARYONIC_BRIDGE="
    "REJECTED_IN_DECLARED_EFT_SCOPE"
)

print(
    "CONFORMAL_SYMMETRON_SCREENING_ALONE_SAVES_MINIMAL_CONSTANT_DISFORMAL_SM_COUPLING="
    "NO"
)

print(
    "CANONICAL_KINETIC_COMPENSATION_TO_014D_Q="
    "CATASTROPHIC_FOR_MACROSCOPIC_WEAK_FIELD_SOURCE"
)

print(
    "REQUIRED_ENVIRONMENTAL_DISFORMAL_HIERARCHY="
    f"{MIN_B_OPERATING_OVER_B_DENSE:.16e}"
)

print(
    "REQUIRED_ENVIRONMENTAL_DELTA_LN_B="
    f"{MIN_DELTA_LN_B:.16e}"
)

print(
    "ENVIRONMENT_DEPENDENT_DISFORMAL_OR_UV_COMPLETION_GENERAL_NO_GO="
    "NO"
)

print(
    "ORDINARY_BARYONIC_LOCAL_TOTAL_FORCE_REVERSAL="
    "NOT_ESTABLISHED"
)

print(
    "PRACTICAL_BARYONIC_ANTIGRAVITY_DEVICE="
    "NO"
)

print(
    "CLAIM_CLASSIFICATION="
    "PROJECT_DERIVED_BARYONIC_DISFORMAL_BRIDGE_FEASIBILITY_BOUND"
)

print(
    "NEXT="
    "UPDATE_DOCS_PRESERVE_014D_AND_RECORD_MINIMAL_BARYONIC_BRIDGE_FAILURE"
)

print(
    "FUTURE_REOPEN_CONDITION="
    "EXPLICIT_ENVIRONMENT_DEPENDENT_OR_UV_COMPLETE_BARYONIC_DISFORMAL_MODEL_WITH_CONSTRAINT_EVASION"
)

print(
    "014E_BARYONIC_DISFORMAL_BRIDGE_GATE="
    "GREEN"
)
