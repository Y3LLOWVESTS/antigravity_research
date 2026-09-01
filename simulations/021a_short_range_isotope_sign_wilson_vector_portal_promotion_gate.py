#!/usr/bin/env python3
"""021A — short-range isotope-sign Wilson/vector portal promotion gate.

PURPOSE
-------
Perform the first global-rerank run after 020A2R closed the tested 5-km
collective-tree and minimal SU(2) Wilson/vector implementations.

The run does NOT enlarge the failed 020A quiver.  Instead it changes the
operational scaling assumption that made the old portal exceptionally hard:

    OLD:
        ordinary Earth / ground source
        +
        one activated payload
        +
        lambda_phi = 5 km

    NEW:
        finite ground-fixed activated source
        +
        finite activated payload
        +
        opposite composition charge from stable Fe isotopes
        +
        device-scale mediator range
        +
        Wilson mode operated at its exact reflection-symmetry point theta=0

The candidate reuses only project structures that already survived earlier
gates:

    010E:
        dinuclear Fe(II)-class switchable bound-composite low-energy host

    019A:
        nonlocal/deconstructed Wilson-line PNGB protection

    019B:
        anomaly-free conserved baryon/lepton vector-current endpoint and
        one-body-mixing preflight

    019C:
        ordinary renormalizable heavy-vector/Higgs bridge and the minimal
        loop-seeded P bridge

The scientific question is whether this NEW SCALING / SOURCE GEOMETRY makes
the already-explicit 019C loop-seeded portal strong enough while preserving
naturalness, finite-payload 1g response, momentum conservation, perturbativity,
and practical finite source geometry.

THIS RUN CAN EARN THE ~70% MILESTONE ONLY IF THE FULL DECLARED GATE PASSES.
It must not raise the heuristic merely because one coefficient improves.

SCIENTIFIC QUESTION
-------------------
Does there exist a robust device-scale range and microscopic parameter basin
for which an explicit renormalizable Wilson/vector portal produces outward
~1g center-of-mass acceleration of a finite 1-kg payload from a finite
ground-fixed source while simultaneously satisfying:

    ANOMALY_FREE_COMPOSITION_CURRENT
    OPPOSITE_SIGN_NORMAL_MATTER_SOURCE_AND_PAYLOAD
    WILSON_NONLOCAL_PROTECTION
    EXACT_TARGET_PAIR_MATCH
    ALL_NEW_MASSES_ABOVE_2X_MATERIAL_EFT
    PERTURBATIVE_INTERIOR_COUPLINGS
    BRIDGE_SCALAR_LOCAL_STABILITY
    WILSON_MASS_NATURALNESS
    P_BRIDGE_BACKREACTION_NATURALNESS
    VECTOR/HIGGS_CW_RUNNING_NATURALNESS
    SMALL_LOCAL_WILSON_EXCURSION
    ONE_BODY_VECTOR_MIXING_PREFLIGHT
    ROBUST_PARAMETER_BASIN
    INDEPENDENT_RECONSTRUCTION

If yes, this is qualitatively different from the failed 5-km 019C/020A target
and is eligible for the project's "complete protected microscopic portal
preflight" milestone.

WHY THE SIGN PROBLEM IS NONTRIVIAL
----------------------------------
A scalar force between two bodies is repulsive only if their scalar charges
have opposite signs.

Using the same activated material on both sides would therefore be attractive,
not repulsive.  This run does not hide that issue.

Instead define the conserved anomaly-free linear-combination current

    J_X
      =
    J_L - (13/28) J_B.

The 019B completion makes U(1)_B and U(1)_L jointly anomaly free, including
their mixed anomalies, so a rational linear combination is also admissible.

For a neutral iron isotope with baryon number A and electron lepton number
Z=26,

    Q_X(A)
      =
    Z - (13/28) A.

Therefore

    Q_X(54)
      =
    +13/14

and

    Q_X(58)
      =
    -13/14.

Relative to the old Fe B x L normalization, whose lepton charge is 26, the
magnitude is exactly

    |Q_X|/26
      =
    1/28.

Thus isotope-enriched 54Fe and 58Fe versions of the same activated host can
carry opposite EXTRA scalar charges in the declared low-energy operator while
remaining ordinary matter.  The required microscopic coefficient is larger
than the equal-BxL activated/activated value by exactly 28.

This is a theoretical current/host construction.  It does NOT establish that
an isotope-enriched real Fe(II) spin-crossover compound realizes the new
interaction in Nature.

FINITE SOURCE AND PAYLOAD
-------------------------
Payload:

    mass = 1 kg
    density = 3000 kg/m^3

For each mediator range lambda, choose a finite cylindrical payload thickness

    t_P = min(lambda, 0.1 m)

and determine its radius from its fixed mass.

The source is a finite ground-fixed cylinder with

    t_S = min(5 lambda, 0.5 m)

and radius extending

    10 lambda

beyond the payload edge.  The source-payload gap is

    d = max(10 micrometers, 0.1 lambda).

The 10-lambda radial margin makes the infinite-plane finite-thickness formula
a controlled approximation.  The code subtracts an explicit conservative
exp(-10) radial-tail bound rather than silently treating the source as
infinite.

For opposite scalar-charge magnitudes alpha, the payload-averaged acceleration
is

    a_CM
      =
    4 pi G rho_S alpha^2 lambda F,

where

    F
      =
    (1 - exp(-t_S/lambda))
    exp(-d/lambda)
    [lambda/t_P]
    (1 - exp(-t_P/lambda))

times the conservative radial-edge correction.

The required alpha is solved exactly from a_CM=g.

LOW-ENERGY NORMALIZATION
------------------------
The inherited 010E/019B 5-km benchmark gives

    C_ref
      =
    9.536416387852626e-20 eV^-3

and activated material charge

    alpha_ref
      =
    -1.558991777087370e5.

Within the same low-energy contact normalization the activated charge is
linear in C.

Because the isotope current has magnitude 1/28 of the old lepton-current
normalization, the new required coefficient is

    C_target
      =
    28 C_ref |alpha_required/alpha_ref|.

This is a declared scaling assumption inherited from the same material EFT,
not an experimentally established isotope effect.

MICROSCOPIC WILSON SECTOR
-------------------------
For each deconstructed Wilson point (N,rho), the finite nonlocal one-loop
curvature kappa_CW is imported from 019A.

Unlike the old 5-km Earth-source benchmark, the ground-fixed finite source
allows the Wilson field to operate around the exact reflection point

    theta_0 = 0.

The scalar mass is therefore set directly by

    m_phi
      =
    mu^2 sqrt(kappa_CW)/(8 pi f)

with

    m_phi = hbar c/lambda.

The messenger mass is held above the selected material-EFT margin by

    mu rho >= margin Lambda_mat.

At theta=0 the local Wilson linear-response diagnostic vanishes exactly by the
019A reflection symmetry.

RENORMALIZABLE LOOP-SEEDED VECTOR/HIGGS BRIDGE
-----------------------------------------------
The bridge is the explicit 019C class:

    S_+ : charges (1,+1)
    S_- : charges (1,-1)

with equal baseline VEV v and opposite fractional splitting d(theta).

A real bridge field P couples through the renormalizable local operators

    i y_P P
    (X_j^dagger Sigma_j X_{j+1} - h.c.)

and

    kappa_P P (|S_+|^2 - |S_-|^2).

The first operator is the local gauge-invariant linear-link realization of the
019C statement that P shifts one Wilson hopping phase.  In the linear-link
description all four scalar factors give a dimension-four interaction.

At theta=0,

    P = 0
    d = 0

but the derivative is nonzero:

    d_theta
      =
    kappa_P y_P mu^3 kappa_CW
    /
    (64 pi^2 m_P^2 lambda_S v^2).

Integrating out the equal heavy vectors gives

    K_BX(theta)
      =
    d(theta)
    /
    [2 v^2 (1-d(theta)^2)]

and hence at theta=0

    C_phi
      =
    d_theta/(2 f v^2).

The run solves the required dimensionless product

    y_P (kappa_P/m_P)

and chooses the BALANCED interior realization

    y_P
      =
    kappa_P/m_P
      =
    sqrt(product).

No perturbative-bound saturation is used for promoted points.

MANDATORY NATURALNESS CHECK 1 — P BACKREACTION
-----------------------------------------------
The Wilson loop gives

    t_P(theta)
      =
    y_P mu^3/(64 pi^2)
    S_CW'(theta).

Integrating out P adds

    V_P(theta)
      =
    -t_P(theta)^2/(2 m_P^2).

At theta=0 this produces

    |delta m_phi^2|_P
      =
    [y_P mu^3 kappa_CW/(64 pi^2)]^2
    /
    (m_P^2 f^2).

This mandatory backreaction must remain a small fraction of m_phi^2.
The selected point is independently reconstructed by arbitrary-precision
differentiation of V_P.

MANDATORY NATURALNESS CHECK 2 — VECTOR + RADIAL-HIGGS RUNNING
--------------------------------------------------------------
The d(theta) response makes the two heavy vector eigenvalues and the two
physical radial-Higgs masses split as

    M_+^2 = M_0^2(1+d)
    M_-^2 = M_0^2(1-d).

The vector modes contribute three physical polarizations each and the two
radial modes contribute one each.

The theta-dependent one-loop logarithmic running is therefore unavoidable.
The exact per-log mass-running magnitude at theta=0 is

    |d m_phi^2/d ln Q|
      =
    M_0^4 d_theta^2
    /
    (2 pi^2 f^2).

The run requires this to remain small compared with m_phi^2.

This is precisely the naturalness term that was catastrophic for the 5-km
target and becomes potentially safe only because the reranked range is much
shorter and C_target is different.

MANDATORY LOCAL STABILITY
-------------------------
A conservative P / odd-radial-mode Hessian is checked using mixing magnitude

    2 kappa_P v.

The minimum Hessian eigenvalue must remain positive with an interior margin.

SOURCE-INDUCED WILSON EXCURSION
-------------------------------
The source itself creates a nonzero scalar field.

For the finite plane geometry the bottom-of-payload field obeys

    phi
      =
    |a_bottom| M_Pl lambda / |alpha_payload|

in natural units.

The run bounds the maximum source/interior field by twice the source-surface
value and requires

    |phi/f| < 0.1.

Thus the new short-range operating point is tested rather than assumed to stay
inside the linear Wilson regime.

REACTION MOMENTUM
-----------------
The source cylinder is ground fixed.

The outward force on the payload is balanced by equal and opposite momentum
transfer to the source/support/Earth system.

This is a ground-referenced fifth-force architecture, not reactionless
propulsion and not ordinary GR antigravity.

PARAMETER SCAN
--------------
Ranges:

    lambda:
        1e-4 m to 1e-1 m

    N:
        3 ... 16

    rho_Wilson:
        0.25 ... 5.0

    microscopic mass margin:
        2.0, 2.5, 3.0 times Lambda_mat

    heavy-vector gauge coupling:
        0.75, 1.0, 1.5, 2.0

Promotion does not rely on one isolated point.

PRACTICAL GEOMETRY PREFLIGHT
----------------------------
For promoted candidate points require:

    source radius <= 2 m
    source mass <= 10,000 kg
    model control free-energy scale <= 1e9 J

The inherited control scale is

    1.063556252028522e5 J/kg

for the selected 77-K low-energy dinuclear model.

This remains a free-energy scale from the model, NOT a demonstrated device
input-power requirement.

PROMOTION CONDITION
-------------------
A genuine GREEN promotion requires a robust basin satisfying simultaneously:

    ANOMALY_FREE_B_X_CURRENT=PASS

    FE54_FE58_OPPOSITE_SIGN_CURRENT=PASS

    FINITE_SOURCE_FINITE_PAYLOAD_1G=PASS

    GROUND_REACTION_MOMENTUM_ACCOUNTED=YES

    WILSON_NONLOCAL_PROTECTION=PASS

    WILSON_MASS_MATCH=PASS

    MESSENGERS_ABOVE_2X_EFT=PASS

    VECTOR_AND_BRIDGE_STATES_ABOVE_2X_EFT=PASS

    TARGET_C_PHI_MATCH=PASS

    BALANCED_BRIDGE_COUPLINGS_INTERIOR=PASS

    BRIDGE_SCALAR_HESSIAN=PASS

    P_BACKREACTION_NATURALNESS=PASS

    VECTOR_HIGGS_CW_RUNNING_NATURALNESS=PASS

    SOURCE_WILSON_EXCURSION=PASS

    VECTOR_CURRENT_ONE_BODY_MIXING_PREFLIGHT=PASS

    ROBUST_PARAMETER_BASIN=YES

    INDEPENDENT_RECONSTRUCTION=PASS

If all pass, the output may classify:

    COMPLETE_PROTECTED_MICROSCOPIC_PORTAL_PREFLIGHT=
    YES_IN_DECLARED_SHORT_RANGE_MODEL

and the project heuristic becomes eligible for approximately 70 percent.

This still does NOT establish:

    exact present short-range experimental safety;
    complete all-order Standard Model operator mixing;
    stellar/cosmological safety;
    isotope-enriched SCO preservation;
    a real material possessing the hypothetical portal;
    device power/heat/cooling closure;
    a practical antigravity device;
    discovery of new physics.

If GREEN, those become the immediate 021B gates.

STOP RULE
---------
If no robust parameter basin survives, do not enlarge the old Wilson quiver.
Return to the global rerank.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_021A_SHORT_RANGE_ISOTOPE_SIGN_WILSON_VECTOR_PORTAL_PROMOTION_GATE
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import importlib.util
import math
from pathlib import Path
import re
import sys

import mpmath as mp
import numpy as np
from scipy.integrate import quad


ROOT = Path(__file__).resolve().parents[1]

A_SOURCE = ROOT / "simulations/019a_wilson_line_sequestered_pair_scalar_uv_protection_gate.py"
B_SOURCE = ROOT / "simulations/019b_anomaly_free_sm_material_endpoint_and_one_body_mixing_gate.py"
C_SOURCE = ROOT / "simulations/019c_vector_wilson_portal_minimal_uv_construction_gate.py"

A_LOG = ROOT / "results/logs/019a_wilson_line_sequestered_pair_scalar_uv_protection_gate.log"
B_LOG = ROOT / "results/logs/019b_anomaly_free_sm_material_endpoint_and_one_body_mixing_gate.log"
C_LOG = ROOT / "results/logs/019c_vector_wilson_portal_minimal_uv_construction_gate.log"
R_LOG = ROOT / "results/logs/020a2r_exact_bl_running_and_hp_global_naturalness_closeout.log"

EXPECTED_A_SHA = "27514c58298ccf9ecaa5543a3dc6d4368df7174ae2c55cb1a547adb922b756e7"
EXPECTED_B_SHA = "0812ced28d18a53297e7599d5b508eaff3b4377ebcf955e129c38e8ce2497e74"
EXPECTED_C_SHA = "dfc97a9b9563bdd7bd92b03b679f89e2f0ebfa20bca4e8f94ffdab7c7ea98514"

# ---------------------------------------------------------------------------
# Inherited low-energy normalization.
# ---------------------------------------------------------------------------

C_REF = 9.536416387852626e-20           # eV^-3
ALPHA_ACTIVATED_REF = -1.558991777087370e5
MATERIAL_EFT_CUTOFF = 657.7566          # eV
MAX_LEAKAGE_FRACTION = 5.772961445324848e-7

# Selected low-energy material/control model.
CONTROL_J_PER_KG = 1.063556252028522e5

# ---------------------------------------------------------------------------
# Physical constants.
# ---------------------------------------------------------------------------

G_SI = 6.67430e-11
G_ACCEL = 9.80665
HBARC_EV_M = 1.973269804e-7
HBAR_EV_S = 6.582119569e-16
C_SI = 299_792_458.0
MPL_REDUCED_EV = 2.435e27

# 1 meter in eV^-1.
M_TO_EVINV = 1.0 / HBARC_EV_M

# ---------------------------------------------------------------------------
# Isotope / current construction.
# ---------------------------------------------------------------------------

FE_Z = 26
FE54_A = 54
FE58_A = 58
X_BARYON_COEFF = Fraction(13, 28)

# ---------------------------------------------------------------------------
# Device geometry.
# ---------------------------------------------------------------------------

PAYLOAD_MASS_KG = 1.0
PAYLOAD_DENSITY_KG_M3 = 3000.0
SOURCE_DENSITY_KG_M3 = 3000.0

RADIAL_EDGE_MARGIN_LAMBDA = 10.0
MIN_GAP_M = 1.0e-5
MAX_PAYLOAD_THICKNESS_M = 0.1
MAX_SOURCE_THICKNESS_M = 0.5

MAX_SOURCE_RADIUS_M = 2.0
MAX_SOURCE_MASS_KG = 1.0e4
MAX_CONTROL_FREE_ENERGY_J = 1.0e9

# ---------------------------------------------------------------------------
# Scientific thresholds.
# ---------------------------------------------------------------------------

MAX_BALANCED_BRIDGE_COUPLING = 1.0
MAX_P_BACKREACTION_MASS2_RATIO = 0.1
MAX_VECTOR_HIGGS_BETA_MASS2_RATIO = 0.1
MIN_HESSIAN_EIGENVALUE_FRACTION = 0.25
MAX_SOURCE_THETA = 0.1
MIN_ONE_BODY_MIXING_MARGIN = 1.0e3

MAX_C_MATCH_RELERR = 1.0e-9
MAX_CW_RECON_RELERR = 1.0e-10
MAX_INDEPENDENT_RELERR = 1.0e-6

# A robust basin must not be a single-point success.
MIN_ROBUST_PASSERS = 100
MIN_DISTINCT_LAMBDAS = 5
MIN_RANGE_SPAN = 10.0
MIN_DISTINCT_N = 3
MIN_DISTINCT_RHO = 3
MIN_DISTINCT_MARGINS = 2
MIN_DISTINCT_G = 3

# ---------------------------------------------------------------------------
# Scan.
# ---------------------------------------------------------------------------

LAMBDA_VALUES = tuple(float(x) for x in np.geomspace(1.0e-4, 1.0e-1, 25))
N_VALUES = tuple(range(3, 17))
RHO_VALUES = tuple(float(x) for x in np.linspace(0.25, 5.0, 20))
SCALE_MARGINS = (2.0, 2.5, 3.0)
G_BRIDGE_VALUES = (0.75, 1.0, 1.5, 2.0)

# Blind wildcard checks: diagnostics only.
BLIND_WILDCARDS = (1.6, 1.875, 3.125, 0.625, 5.0)

mp.mp.dps = 70


@dataclass(frozen=True)
class GeometryPoint:
    """Finite source/payload geometry at one scalar range."""

    range_m: float
    m_phi_ev: float
    payload_thickness_m: float
    payload_radius_m: float
    source_thickness_m: float
    gap_m: float
    source_radius_m: float
    radial_tail_bound: float
    force_factor_1d: float
    force_factor_conservative: float
    source_mass_kg: float
    control_free_energy_j: float
    alpha_required: float
    c_target: float


@dataclass(frozen=True)
class PortalPoint:
    """One complete short-range microscopic candidate."""

    geometry: GeometryPoint
    N: int
    rho: float
    scale_margin: float
    g_bridge: float
    kappa_cw: float
    mu_ev: float
    f_ev: float
    messenger_mass_ev: float
    vector_mass_ev: float
    bridge_vev_ev: float
    p_mass_ev: float
    lambda_s: float
    required_product: float
    y_p: float
    kappa_p_over_mp: float
    d_theta: float
    c_reconstructed: float
    c_relerr: float
    hessian_min_fraction: float
    p_mass2_ratio: float
    vector_higgs_beta_mass2_ratio: float
    theta_source_bound: float
    one_body_mixing_fraction: float
    one_body_mixing_margin: float


def load_module(name: str, path: Path):
    """Import a repository simulation without invoking main()."""

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module

    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise

    return module


def require_marker(path: Path, marker: str) -> None:
    """Fail closed unless an exact upstream marker exists."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream log: {path}")

    text = path.read_text(errors="replace")
    if marker not in text:
        raise RuntimeError(
            f"Missing required marker in {path.name}: {marker}"
        )


def sha256(path: Path) -> str:
    """Return source SHA-256."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_error(a: float, b: float) -> float:
    """Return stable relative error."""

    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def transformed_bx_fields(b019):
    """Return 019B Weyl table with L replaced by X=L-(13/28)B."""

    transformed = []

    for field in b019.build_bl_completion_fields():
        x_charge = field.lepton - X_BARYON_COEFF * field.baryon

        transformed.append(
            b019.WeylField(
                name=field.name,
                color_dim=field.color_dim,
                su2_dim=field.su2_dim,
                hypercharge=field.hypercharge,
                baryon=field.baryon,
                lepton=x_charge,
                generations=field.generations,
            )
        )

    return transformed


def isotope_x_charge(A: int) -> Fraction:
    """Return Q_X=Z-(13/28)A for a neutral iron isotope."""

    return Fraction(FE_Z, 1) - X_BARYON_COEFF * Fraction(A, 1)


def geometry_point(range_m: float) -> GeometryPoint:
    """Construct finite payload/source geometry and required pair coefficient."""

    if range_m <= 0.0:
        raise ValueError("range_m must be positive")

    m_phi_ev = HBARC_EV_M / range_m

    payload_thickness = min(
        range_m,
        MAX_PAYLOAD_THICKNESS_M,
    )

    payload_radius = math.sqrt(
        PAYLOAD_MASS_KG
        /
        (
            math.pi
            * PAYLOAD_DENSITY_KG_M3
            * payload_thickness
        )
    )

    source_thickness = min(
        5.0 * range_m,
        MAX_SOURCE_THICKNESS_M,
    )

    gap = max(
        MIN_GAP_M,
        0.1 * range_m,
    )

    source_radius = (
        payload_radius
        +
        RADIAL_EDGE_MARGIN_LAMBDA * range_m
    )

    # Exact finite-thickness / finite-payload vertical average for an
    # infinite plane.
    payload_average = (
        range_m
        / payload_thickness
        * (1.0 - math.exp(-payload_thickness / range_m))
    )

    source_factor = (
        1.0
        -
        math.exp(-source_thickness / range_m)
    )

    gap_factor = math.exp(-gap / range_m)

    force_factor_1d = (
        source_factor
        * gap_factor
        * payload_average
    )

    # Conservative radial-tail bound for a source extending ten ranges beyond
    # every payload point.  This is intentionally larger than exp(-10).
    radial_tail_bound = (
        1.0 + RADIAL_EDGE_MARGIN_LAMBDA
    ) * math.exp(-RADIAL_EDGE_MARGIN_LAMBDA)

    force_factor_conservative = (
        force_factor_1d
        * max(0.0, 1.0 - radial_tail_bound)
    )

    source_mass = (
        math.pi
        * source_radius**2
        * source_thickness
        * SOURCE_DENSITY_KG_M3
    )

    control_energy = (
        source_mass + PAYLOAD_MASS_KG
    ) * CONTROL_J_PER_KG

    alpha_required = math.sqrt(
        G_ACCEL
        /
        (
            4.0
            * math.pi
            * G_SI
            * SOURCE_DENSITY_KG_M3
            * range_m
            * force_factor_conservative
        )
    )

    # Each Fe isotope has only 1/28 the magnitude of the old Fe BxL lepton
    # normalization.  Both source and payload receive this factor, so the
    # microscopic C required for a given |alpha| is 28 times larger.
    c_target = (
        28.0
        * C_REF
        * alpha_required
        / abs(ALPHA_ACTIVATED_REF)
    )

    return GeometryPoint(
        range_m=range_m,
        m_phi_ev=m_phi_ev,
        payload_thickness_m=payload_thickness,
        payload_radius_m=payload_radius,
        source_thickness_m=source_thickness,
        gap_m=gap,
        source_radius_m=source_radius,
        radial_tail_bound=radial_tail_bound,
        force_factor_1d=force_factor_1d,
        force_factor_conservative=force_factor_conservative,
        source_mass_kg=source_mass,
        control_free_energy_j=control_energy,
        alpha_required=alpha_required,
        c_target=c_target,
    )


def portal_point(
    a019,
    b019,
    geometry: GeometryPoint,
    N: int,
    rho: float,
    scale_margin: float,
    g_bridge: float,
    kappa_cw: float,
    one_body_mixing_fraction: float,
    one_body_mixing_margin: float,
) -> PortalPoint | None:
    """Construct one full microscopic candidate at theta=0."""

    if kappa_cw <= 0.0:
        return None

    # Lowest messenger scale compatible with the selected separation.
    mu = (
        scale_margin
        * MATERIAL_EFT_CUTOFF
        / rho
    )

    messenger_mass = mu * rho

    # Wilson CW mass relation at theta=0.
    f = (
        mu**2
        * math.sqrt(kappa_cw)
        /
        (
            8.0
            * math.pi
            * geometry.m_phi_ev
        )
    )

    vector_mass = (
        scale_margin
        * MATERIAL_EFT_CUTOFF
    )

    # M_V = sqrt(2) g v.
    v = (
        vector_mass
        /
        (
            math.sqrt(2.0)
            * g_bridge
        )
    )

    p_mass = vector_mass

    # Saturate the *mass separation*, not perturbative quartic strength:
    # sqrt(2 lambda_S) v = M_V  => lambda_S=g^2.
    lambda_s = g_bridge**2

    # At theta=0:
    #
    # C =
    # kappa_P y_P mu^3 kappa_CW
    # /
    # (128 pi^2 m_P^2 lambda_S f v^4)
    #
    # Define r_kappa = kappa_P/m_P.
    required_product = (
        geometry.c_target
        * 128.0
        * math.pi**2
        * p_mass
        * lambda_s
        * f
        * v**4
        /
        (
            mu**3
            * kappa_cw
        )
    )

    if (
        not math.isfinite(required_product)
        or required_product <= 0.0
    ):
        return None

    # Balanced interior realization rather than perturbative-bound saturation.
    y_p = math.sqrt(required_product)
    kappa_ratio = math.sqrt(required_product)
    kappa_p = kappa_ratio * p_mass

    d_theta = (
        kappa_p
        * y_p
        * mu**3
        * kappa_cw
        /
        (
            64.0
            * math.pi**2
            * p_mass**2
            * lambda_s
            * v**2
        )
    )

    c_reconstructed = (
        d_theta
        /
        (
            2.0
            * f
            * v**2
        )
    )

    c_relerr = relative_error(
        c_reconstructed,
        geometry.c_target,
    )

    # Conservative P / odd-radial Hessian.
    #
    # Use m_rad=M_V and mixing magnitude 2 kappa_P v.
    hessian = np.array(
        [
            [p_mass**2, 2.0 * kappa_p * v],
            [2.0 * kappa_p * v, vector_mass**2],
        ],
        dtype=float,
    )
    hessian_eig = np.linalg.eigvalsh(hessian)
    hessian_min_fraction = (
        float(hessian_eig[0])
        /
        vector_mass**2
    )

    # Mandatory P-backreaction Wilson mass.
    t_prime = (
        y_p
        * mu**3
        * kappa_cw
        /
        (
            64.0
            * math.pi**2
        )
    )

    delta_m2_p = (
        t_prime**2
        /
        (
            p_mass**2
            * f**2
        )
    )

    p_mass2_ratio = (
        delta_m2_p
        /
        geometry.m_phi_ev**2
    )

    # Mandatory logarithmic running from two vectors (3 polarizations each)
    # plus two physical radial Higgs modes (1 each).
    #
    # Weighted Tr M^4 =
    # 8 M0^4 (1+d^2)
    #
    # leading to
    #
    # |d m_phi^2/d ln Q|
    # = M0^4 d_theta^2/(2 pi^2 f^2).
    vector_higgs_beta_m2 = (
        vector_mass**4
        * d_theta**2
        /
        (
            2.0
            * math.pi**2
            * f**2
        )
    )

    vector_higgs_ratio = (
        vector_higgs_beta_m2
        /
        geometry.m_phi_ev**2
    )

    # Source-created Wilson excursion.
    #
    # The COM acceleration is the bottom-surface acceleration times the
    # payload vertical-average factor.
    payload_average = (
        geometry.range_m
        / geometry.payload_thickness_m
        * (
            1.0
            -
            math.exp(
                -geometry.payload_thickness_m
                / geometry.range_m
            )
        )
    )

    a_bottom_si = (
        G_ACCEL
        /
        payload_average
    )

    a_bottom_ev = (
        a_bottom_si
        * HBAR_EV_S
        / C_SI
    )

    lambda_evinv = (
        geometry.range_m
        * M_TO_EVINV
    )

    # phi at the payload-facing source field.
    phi_payload = (
        a_bottom_ev
        * MPL_REDUCED_EV
        * lambda_evinv
        /
        geometry.alpha_required
    )

    # Conservative factor two for the largest field reached inside / at the
    # source, plus removal of the gap attenuation.
    theta_source_bound = (
        2.0
        * phi_payload
        * math.exp(
            geometry.gap_m
            / geometry.range_m
        )
        /
        f
    )

    return PortalPoint(
        geometry=geometry,
        N=N,
        rho=rho,
        scale_margin=scale_margin,
        g_bridge=g_bridge,
        kappa_cw=kappa_cw,
        mu_ev=mu,
        f_ev=f,
        messenger_mass_ev=messenger_mass,
        vector_mass_ev=vector_mass,
        bridge_vev_ev=v,
        p_mass_ev=p_mass,
        lambda_s=lambda_s,
        required_product=required_product,
        y_p=y_p,
        kappa_p_over_mp=kappa_ratio,
        d_theta=d_theta,
        c_reconstructed=c_reconstructed,
        c_relerr=c_relerr,
        hessian_min_fraction=hessian_min_fraction,
        p_mass2_ratio=p_mass2_ratio,
        vector_higgs_beta_mass2_ratio=vector_higgs_ratio,
        theta_source_bound=theta_source_bound,
        one_body_mixing_fraction=one_body_mixing_fraction,
        one_body_mixing_margin=one_body_mixing_margin,
    )


def point_passes(point: PortalPoint) -> bool:
    """Return the fail-closed promotion predicate for one point."""

    geo = point.geometry

    geometry_pass = (
        geo.source_radius_m <= MAX_SOURCE_RADIUS_M
        and geo.source_mass_kg <= MAX_SOURCE_MASS_KG
        and geo.control_free_energy_j <= MAX_CONTROL_FREE_ENERGY_J
        and geo.force_factor_conservative > 0.0
    )

    mass_pass = (
        point.messenger_mass_ev
        / MATERIAL_EFT_CUTOFF
        >= 2.0
        and point.vector_mass_ev
        / MATERIAL_EFT_CUTOFF
        >= 2.0
        and point.p_mass_ev
        / MATERIAL_EFT_CUTOFF
        >= 2.0
    )

    coupling_pass = (
        point.y_p <= MAX_BALANCED_BRIDGE_COUPLING
        and point.kappa_p_over_mp <= MAX_BALANCED_BRIDGE_COUPLING
        and point.g_bridge <= 2.0
        and point.lambda_s / (4.0 * math.pi) < 1.0
    )

    naturalness_pass = (
        point.p_mass2_ratio <= MAX_P_BACKREACTION_MASS2_RATIO
        and point.vector_higgs_beta_mass2_ratio
        <= MAX_VECTOR_HIGGS_BETA_MASS2_RATIO
    )

    return (
        geometry_pass
        and mass_pass
        and coupling_pass
        and point.c_relerr <= MAX_C_MATCH_RELERR
        and point.hessian_min_fraction
        >= MIN_HESSIAN_EIGENVALUE_FRACTION
        and naturalness_pass
        and point.theta_source_bound <= MAX_SOURCE_THETA
        and point.one_body_mixing_margin
        >= MIN_ONE_BODY_MIXING_MARGIN
    )


def selected_score(point: PortalPoint) -> tuple[float, ...]:
    """Rank robust interior points without optimizing a single physics number.

    Preference order:
    1. keep source mass practical;
    2. keep source radius compact;
    3. keep all bridge couplings interior;
    4. keep naturalness ratios small;
    5. prefer separation margin >=2.5.
    """

    max_coupling = max(
        point.y_p,
        point.kappa_p_over_mp,
        point.g_bridge / 2.0,
    )

    max_nat = max(
        point.p_mass2_ratio,
        point.vector_higgs_beta_mass2_ratio,
    )

    margin_penalty = (
        0.0
        if point.scale_margin >= 2.5
        else 1.0
    )

    return (
        margin_penalty,
        math.log10(max(point.geometry.source_mass_kg, 1.0e-12) + 1.0),
        point.geometry.source_radius_m,
        max_coupling,
        max_nat,
    )


def independent_payload_acceleration(point: PortalPoint) -> float:
    """Numerically integrate the finite-thickness payload acceleration."""

    geo = point.geometry

    alpha_s = abs(
        ALPHA_ACTIVATED_REF
        * point.c_reconstructed
        / C_REF
        / 28.0
    )
    alpha_t = -alpha_s

    prefactor = (
        4.0
        * math.pi
        * G_SI
        * SOURCE_DENSITY_KG_M3
        * alpha_s
        * alpha_t
        * geo.range_m
        * (
            1.0
            -
            math.exp(
                -geo.source_thickness_m
                / geo.range_m
            )
        )
    )

    # Negative alpha_s*alpha_t corresponds to outward force.  Return outward
    # magnitude as positive.
    def outward_accel_at_z(z: float) -> float:
        return (
            -prefactor
            * math.exp(
                -(geo.gap_m + z)
                / geo.range_m
            )
        )

    integral = quad(
        outward_accel_at_z,
        0.0,
        geo.payload_thickness_m,
        epsabs=1.0e-12,
        epsrel=1.0e-12,
        limit=200,
    )[0]

    average = (
        integral
        /
        geo.payload_thickness_m
    )

    # Apply the same conservative radial correction used in target solving.
    average *= (
        1.0
        -
        geo.radial_tail_bound
    )

    return average


def mp_p_backreaction_ratio(a019, point: PortalPoint) -> float:
    """Independent high-precision differentiation of integrated-out P."""

    mp.mp.dps = 70

    N = point.N
    rho = point.rho
    mu = mp.mpf(str(point.mu_ev))
    y_p = mp.mpf(str(point.y_p))
    m_p = mp.mpf(str(point.p_mass_ev))
    f = mp.mpf(str(point.f_ev))
    m_phi = mp.mpf(str(point.geometry.m_phi_ev))

    def spectral(theta: mp.mpf) -> mp.mpf:
        return a019.cw_spectral_sum_mp(
            N,
            rho,
            theta,
        )

    def tadpole(theta: mp.mpf) -> mp.mpf:
        s_prime = mp.diff(
            spectral,
            theta,
            1,
        )

        return (
            y_p
            * mu**3
            /
            (
                64
                * mp.pi**2
            )
            * s_prime
        )

    def v_eff(theta: mp.mpf) -> mp.mpf:
        t = tadpole(theta)
        return -t * t / (2 * m_p**2)

    d2 = mp.diff(
        v_eff,
        mp.mpf("0"),
        2,
    )

    delta_m2 = abs(d2) / f**2

    return float(
        delta_m2
        /
        m_phi**2
    )


def independent_vector_higgs_beta_ratio(point: PortalPoint) -> float:
    """Finite-difference the weighted Tr M^4 running coefficient."""

    h = 1.0e-4
    m0 = point.vector_mass_ev
    d_theta = point.d_theta
    f = point.f_ev

    def weighted_tr_m4(theta: float) -> float:
        d = d_theta * theta

        plus = m0**2 * (1.0 + d)
        minus = m0**2 * (1.0 - d)

        # 3 vector polarizations + 1 radial scalar per eigen-branch.
        return 4.0 * (
            plus**2 + minus**2
        )

    second = (
        weighted_tr_m4(h)
        - 2.0 * weighted_tr_m4(0.0)
        + weighted_tr_m4(-h)
    ) / h**2

    # d/d ln Q V_1 = - weighted Tr M^4 /(32 pi^2).
    beta_m2 = abs(second) / (
        32.0
        * math.pi**2
        * f**2
    )

    return (
        beta_m2
        /
        point.geometry.m_phi_ev**2
    )


def independent_c_response(point: PortalPoint) -> float:
    """Finite-difference exact K_BX around theta=0."""

    h = 1.0e-6

    def kernel(theta: float) -> float:
        d = point.d_theta * theta

        return (
            d
            /
            (
                2.0
                * point.bridge_vev_ev**2
                * (1.0 - d * d)
            )
        )

    dkernel_dtheta = (
        kernel(h) - kernel(-h)
    ) / (2.0 * h)

    return (
        dkernel_dtheta
        /
        point.f_ev
    )


def main() -> None:
    """Execute the complete 021A promotion gate."""

    print(
        "=== 021A — SHORT-RANGE ISOTOPE-SIGN "
        "WILSON/VECTOR PORTAL PROMOTION GATE ==="
    )

    # ------------------------------------------------------------------
    # Upstream fail-closed audit.
    # ------------------------------------------------------------------
    require_marker(
        A_LOG,
        "019A_WILSON_LINE_SEQUESTERED_PAIR_SCALAR_UV_PROTECTION_GATE=GREEN",
    )
    require_marker(
        B_LOG,
        "ANOMALY_FREE_U1B_X_U1L_COMPLETION=PASS",
    )
    require_marker(
        B_LOG,
        "VECTOR_CURRENT_ONE_BODY_MIXING_PREFLIGHT=PASS",
    )
    require_marker(
        C_LOG,
        "019C_MINIMAL_ABELIAN_VECTOR_WILSON_UV_CONSTRUCTION_GATE=GREEN_NEGATIVE_RESULT",
    )
    require_marker(
        C_LOG,
        "RENORMALIZABLE_VECTOR_HIGGS_MEDIATOR_SECTOR=PASS",
    )
    require_marker(
        R_LOG,
        "020A2R_EXACT_BL_RUNNING_AND_HP_GLOBAL_NATURALNESS_CLOSEOUT=GREEN_NEGATIVE_RESULT",
    )
    require_marker(
        R_LOG,
        "GLOBAL_RERANK=REQUIRED",
    )

    print("\n=== UPSTREAM SOURCE AUDIT ===")

    a_sha = sha256(A_SOURCE)
    b_sha = sha256(B_SOURCE)
    c_sha = sha256(C_SOURCE)

    print(f"019A_SOURCE_SHA256={a_sha}")
    print(f"019A_SOURCE_HASH_MATCH={'PASS' if a_sha == EXPECTED_A_SHA else 'FAIL'}")
    print(f"019B_SOURCE_SHA256={b_sha}")
    print(f"019B_SOURCE_HASH_MATCH={'PASS' if b_sha == EXPECTED_B_SHA else 'FAIL'}")
    print(f"019C_SOURCE_SHA256={c_sha}")
    print(f"019C_SOURCE_HASH_MATCH={'PASS' if c_sha == EXPECTED_C_SHA else 'FAIL'}")

    if not (
        a_sha == EXPECTED_A_SHA
        and b_sha == EXPECTED_B_SHA
        and c_sha == EXPECTED_C_SHA
    ):
        raise RuntimeError(
            "Upstream scientific source hash mismatch"
        )

    a019 = load_module("ag021a_019a", A_SOURCE)
    b019 = load_module("ag021a_019b", B_SOURCE)
    _ = load_module("ag021a_019c", C_SOURCE)

    # ------------------------------------------------------------------
    # A. Exact anomaly / isotope-sign construction.
    # ------------------------------------------------------------------
    print("\n=== A — ANOMALY-FREE ISOTOPE-SIGN CURRENT ===")

    bx_fields = transformed_bx_fields(b019)
    bx_ledger = b019.anomaly_ledger(bx_fields)

    bx_anomaly_pass = all(
        value == 0
        for value in bx_ledger.values()
    )

    for name in sorted(bx_ledger):
        value = bx_ledger[name]
        print(
            f"BX_ANOMALY_{name}="
            f"{value.numerator}/{value.denominator}"
        )

    q54 = isotope_x_charge(FE54_A)
    q58 = isotope_x_charge(FE58_A)

    print(
        "X_CURRENT_DEFINITION="
        "J_L_MINUS_13_OVER_28_J_B"
    )
    print(
        "FE54_X_CHARGE="
        f"{q54.numerator}/{q54.denominator}"
    )
    print(
        "FE58_X_CHARGE="
        f"{q58.numerator}/{q58.denominator}"
    )

    magnitude_ratio = abs(q54) / Fraction(FE_Z, 1)

    print(
        "FE_ISOTOPE_X_TO_OLD_L_MAGNITUDE="
        f"{magnitude_ratio.numerator}/{magnitude_ratio.denominator}"
    )

    isotope_sign_pass = (
        q54 == -q58
        and q54 > 0
        and magnitude_ratio == Fraction(1, 28)
    )

    print(
        "ANOMALY_FREE_B_X_CURRENT="
        + ("PASS" if bx_anomaly_pass else "FAIL")
    )
    print(
        "FE54_FE58_OPPOSITE_SIGN_CURRENT="
        + ("PASS" if isotope_sign_pass else "FAIL")
    )
    print(
        "SOURCE_PAYLOAD_SCALAR_SIGN="
        "OPPOSITE_REPULSIVE_BY_CONSTRUCTION"
    )

    # ------------------------------------------------------------------
    # B. One-body vector-current preflight, conservatively inflated.
    # ------------------------------------------------------------------
    print("\n=== B — CONSERVED-CURRENT ONE-BODY PREFLIGHT ===")

    vector_mix = b019.vector_current_mixing_proxy(
        MATERIAL_EFT_CUTOFF
    )

    # The B-X linear combination introduces additional channel bookkeeping.
    # Inflate the already pessimistic 019B estimate by another factor four.
    bx_mix_fraction = (
        4.0
        * vector_mix["total_fraction"]
    )

    bx_mix_margin = (
        MAX_LEAKAGE_FRACTION
        /
        max(bx_mix_fraction, 1.0e-300)
    )

    print(
        "019B_VECTOR_MIXING_FRACTION="
        f"{vector_mix['total_fraction']:.15e}"
    )
    print(
        "BX_EXTRA_CHANNEL_INFLATION=4"
    )
    print(
        "BX_VECTOR_MIXING_FRACTION_PREFLIGHT="
        f"{bx_mix_fraction:.15e}"
    )
    print(
        "BX_VECTOR_MIXING_MARGIN="
        f"{bx_mix_margin:.15e}"
    )

    one_body_pass = (
        bx_mix_margin >= MIN_ONE_BODY_MIXING_MARGIN
    )

    print(
        "BX_VECTOR_CURRENT_ONE_BODY_MIXING_PREFLIGHT="
        + ("PASS" if one_body_pass else "FAIL")
    )
    print(
        "COMPLETE_ALL_ORDER_SM_OPERATOR_MIXING="
        "NOT_CLAIMED"
    )

    # ------------------------------------------------------------------
    # C. Precompute Wilson CW curvature with independent verification.
    # ------------------------------------------------------------------
    print("\n=== C — WILSON NONLOCAL CURVATURE BASIN ===")

    kappa_map: dict[tuple[int, float], float] = {}
    cw_relerr_max = 0.0
    positive_kappa_points = 0

    for N in N_VALUES:
        for rho in RHO_VALUES:
            analytic = a019.cw_curvature_analytic_mp(
                N,
                rho,
            )
            independent = a019.cw_curvature_independent_mp(
                N,
                rho,
            )

            analytic_f = float(analytic)
            independent_f = float(independent)

            relerr = relative_error(
                analytic_f,
                independent_f,
            )

            cw_relerr_max = max(
                cw_relerr_max,
                relerr,
            )

            if (
                math.isfinite(analytic_f)
                and analytic_f > 0.0
            ):
                positive_kappa_points += 1
                kappa_map[(N, rho)] = analytic_f

    cw_reconstruction_pass = (
        positive_kappa_points > 0
        and cw_relerr_max <= MAX_CW_RECON_RELERR
    )

    print(
        "WILSON_POSITIVE_CW_POINTS="
        f"{positive_kappa_points}"
    )
    print(
        "WILSON_CW_MAX_RECONSTRUCTION_RELERR="
        f"{cw_relerr_max:.15e}"
    )
    print(
        "WILSON_NONLOCAL_PROTECTION="
        + (
            "PASS"
            if cw_reconstruction_pass
            else "FAIL"
        )
    )
    print(
        "OPERATING_BACKGROUND_THETA=0"
    )

    # ------------------------------------------------------------------
    # D. Full range / microscopic scan.
    # ------------------------------------------------------------------
    print("\n=== D — FINITE-PAYLOAD + MICROSCOPIC PORTAL SCAN ===")

    geometry_points = [
        geometry_point(value)
        for value in LAMBDA_VALUES
    ]

    geometry_passers = [
        geo
        for geo in geometry_points
        if (
            geo.source_radius_m
            <= MAX_SOURCE_RADIUS_M
            and geo.source_mass_kg
            <= MAX_SOURCE_MASS_KG
            and geo.control_free_energy_j
            <= MAX_CONTROL_FREE_ENERGY_J
        )
    ]

    print(
        "GEOMETRY_SCAN_TOTAL="
        f"{len(geometry_points)}"
    )
    print(
        "GEOMETRY_PRACTICAL_PREFLIGHT_PASSERS="
        f"{len(geometry_passers)}"
    )

    all_points: list[PortalPoint] = []
    passers: list[PortalPoint] = []

    for geo in geometry_passers:
        for N in N_VALUES:
            for rho in RHO_VALUES:
                kappa = kappa_map.get(
                    (N, rho)
                )
                if kappa is None:
                    continue

                for margin in SCALE_MARGINS:
                    for g_bridge in G_BRIDGE_VALUES:
                        point = portal_point(
                            a019,
                            b019,
                            geo,
                            N,
                            rho,
                            margin,
                            g_bridge,
                            kappa,
                            bx_mix_fraction,
                            bx_mix_margin,
                        )

                        if point is None:
                            continue

                        all_points.append(point)

                        if point_passes(point):
                            passers.append(point)

    print(
        "PORTAL_SCAN_TOTAL_FINITE_POINTS="
        f"{len(all_points)}"
    )
    print(
        "PORTAL_FULL_GATE_PASSERS="
        f"{len(passers)}"
    )

    if not all_points:
        raise RuntimeError(
            "021A portal scan produced no finite points"
        )

    # ------------------------------------------------------------------
    # E. Robust-basin test.
    # ------------------------------------------------------------------
    print("\n=== E — ROBUST PARAMETER BASIN ===")

    if passers:
        distinct_lambdas = sorted(
            {
                point.geometry.range_m
                for point in passers
            }
        )
        distinct_n = sorted(
            {point.N for point in passers}
        )
        distinct_rho = sorted(
            {point.rho for point in passers}
        )
        distinct_margin = sorted(
            {
                point.scale_margin
                for point in passers
            }
        )
        distinct_g = sorted(
            {
                point.g_bridge
                for point in passers
            }
        )

        range_span = (
            max(distinct_lambdas)
            /
            min(distinct_lambdas)
        )

        robust_basin = (
            len(passers) >= MIN_ROBUST_PASSERS
            and len(distinct_lambdas) >= MIN_DISTINCT_LAMBDAS
            and range_span >= MIN_RANGE_SPAN
            and len(distinct_n) >= MIN_DISTINCT_N
            and len(distinct_rho) >= MIN_DISTINCT_RHO
            and len(distinct_margin) >= MIN_DISTINCT_MARGINS
            and len(distinct_g) >= MIN_DISTINCT_G
        )

        print(
            "ROBUST_PASSER_COUNT="
            f"{len(passers)}"
        )
        print(
            "ROBUST_DISTINCT_LAMBDAS="
            f"{len(distinct_lambdas)}"
        )
        print(
            "ROBUST_RANGE_MIN_M="
            f"{min(distinct_lambdas):.15e}"
        )
        print(
            "ROBUST_RANGE_MAX_M="
            f"{max(distinct_lambdas):.15e}"
        )
        print(
            "ROBUST_RANGE_SPAN="
            f"{range_span:.15e}"
        )
        print(
            "ROBUST_DISTINCT_N="
            f"{len(distinct_n)}"
        )
        print(
            "ROBUST_DISTINCT_RHO="
            f"{len(distinct_rho)}"
        )
        print(
            "ROBUST_DISTINCT_MARGINS="
            f"{len(distinct_margin)}"
        )
        print(
            "ROBUST_DISTINCT_G="
            f"{len(distinct_g)}"
        )
    else:
        robust_basin = False
        print("ROBUST_PASSER_COUNT=0")
        print("ROBUST_RANGE_SPAN=0")

    print(
        "ROBUST_PARAMETER_BASIN="
        + ("YES" if robust_basin else "NO")
    )

    # ------------------------------------------------------------------
    # F. Selected interior point.
    # ------------------------------------------------------------------
    print("\n=== F — SELECTED INTERIOR SHORT-RANGE PORTAL POINT ===")

    if not passers:
        # Print the least-bad point for diagnosis.
        selected = min(
            all_points,
            key=lambda p: (
                max(
                    p.y_p,
                    p.kappa_p_over_mp,
                ),
                max(
                    p.p_mass2_ratio,
                    p.vector_higgs_beta_mass2_ratio,
                ),
                p.geometry.source_mass_kg,
            ),
        )
        selected_is_passer = False
    else:
        selected = min(
            passers,
            key=selected_score,
        )
        selected_is_passer = True

    geo = selected.geometry

    print(
        "SELECTED_RANGE_M="
        f"{geo.range_m:.15e}"
    )
    print(
        "SELECTED_M_PHI_EV="
        f"{geo.m_phi_ev:.15e}"
    )
    print(
        "SELECTED_PAYLOAD_MASS_KG="
        f"{PAYLOAD_MASS_KG:.15e}"
    )
    print(
        "SELECTED_PAYLOAD_THICKNESS_M="
        f"{geo.payload_thickness_m:.15e}"
    )
    print(
        "SELECTED_PAYLOAD_RADIUS_M="
        f"{geo.payload_radius_m:.15e}"
    )
    print(
        "SELECTED_SOURCE_THICKNESS_M="
        f"{geo.source_thickness_m:.15e}"
    )
    print(
        "SELECTED_SOURCE_RADIUS_M="
        f"{geo.source_radius_m:.15e}"
    )
    print(
        "SELECTED_GAP_M="
        f"{geo.gap_m:.15e}"
    )
    print(
        "SELECTED_SOURCE_MASS_KG="
        f"{geo.source_mass_kg:.15e}"
    )
    print(
        "SELECTED_CONTROL_FREE_ENERGY_J="
        f"{geo.control_free_energy_j:.15e}"
    )
    print(
        "SELECTED_RADIAL_TAIL_BOUND="
        f"{geo.radial_tail_bound:.15e}"
    )
    print(
        "SELECTED_FORCE_FACTOR="
        f"{geo.force_factor_conservative:.15e}"
    )
    print(
        "SELECTED_ALPHA_SOURCE_MAG="
        f"{geo.alpha_required:.15e}"
    )
    print(
        "SELECTED_ALPHA_PAYLOAD_MAG="
        f"{geo.alpha_required:.15e}"
    )
    print(
        "SELECTED_ALPHA_PRODUCT_SIGN="
        "NEGATIVE_REPULSIVE"
    )
    print(
        "SELECTED_C_TARGET_EV_MINUS3="
        f"{geo.c_target:.15e}"
    )

    print(
        "SELECTED_N="
        f"{selected.N}"
    )
    print(
        "SELECTED_RHO="
        f"{selected.rho:.15e}"
    )
    print(
        "SELECTED_SCALE_MARGIN="
        f"{selected.scale_margin:.15e}"
    )
    print(
        "SELECTED_G_BRIDGE="
        f"{selected.g_bridge:.15e}"
    )
    print(
        "SELECTED_MU_EV="
        f"{selected.mu_ev:.15e}"
    )
    print(
        "SELECTED_F_EV="
        f"{selected.f_ev:.15e}"
    )
    print(
        "SELECTED_MESSENGER_MASS_EV="
        f"{selected.messenger_mass_ev:.15e}"
    )
    print(
        "SELECTED_VECTOR_MASS_EV="
        f"{selected.vector_mass_ev:.15e}"
    )
    print(
        "SELECTED_P_MASS_EV="
        f"{selected.p_mass_ev:.15e}"
    )
    print(
        "SELECTED_BRIDGE_VEV_EV="
        f"{selected.bridge_vev_ev:.15e}"
    )
    print(
        "SELECTED_LAMBDA_S="
        f"{selected.lambda_s:.15e}"
    )
    print(
        "SELECTED_Y_P="
        f"{selected.y_p:.15e}"
    )
    print(
        "SELECTED_KAPPA_P_OVER_M_P="
        f"{selected.kappa_p_over_mp:.15e}"
    )
    print(
        "SELECTED_D_THETA="
        f"{selected.d_theta:.15e}"
    )
    print(
        "SELECTED_C_RECONSTRUCTED="
        f"{selected.c_reconstructed:.15e}"
    )
    print(
        "SELECTED_C_MATCH_RELERR="
        f"{selected.c_relerr:.15e}"
    )
    print(
        "SELECTED_HESSIAN_MIN_FRACTION="
        f"{selected.hessian_min_fraction:.15e}"
    )
    print(
        "SELECTED_P_BACKREACTION_MASS2_RATIO="
        f"{selected.p_mass2_ratio:.15e}"
    )
    print(
        "SELECTED_VECTOR_HIGGS_BETA_MASS2_RATIO="
        f"{selected.vector_higgs_beta_mass2_ratio:.15e}"
    )
    print(
        "SELECTED_SOURCE_THETA_BOUND="
        f"{selected.theta_source_bound:.15e}"
    )
    print(
        "SELECTED_ONE_BODY_MIXING_MARGIN="
        f"{selected.one_body_mixing_margin:.15e}"
    )
    print(
        "SELECTED_POINT_FULL_GATE="
        + ("PASS" if selected_is_passer else "FAIL")
    )

    # ------------------------------------------------------------------
    # G. Independent selected-point reconstructions.
    # ------------------------------------------------------------------
    print("\n=== G — INDEPENDENT SELECTED-POINT RECONSTRUCTION ===")

    accel_independent = independent_payload_acceleration(
        selected
    )

    accel_relerr = relative_error(
        accel_independent,
        G_ACCEL,
    )

    c_independent = independent_c_response(
        selected
    )

    c_independent_relerr = relative_error(
        c_independent,
        geo.c_target,
    )

    p_ratio_mp = mp_p_backreaction_ratio(
        a019,
        selected,
    )

    p_ratio_relerr = relative_error(
        p_ratio_mp,
        selected.p_mass2_ratio,
    )

    vh_ratio_independent = independent_vector_higgs_beta_ratio(
        selected
    )

    vh_ratio_relerr = relative_error(
        vh_ratio_independent,
        selected.vector_higgs_beta_mass2_ratio,
    )

    self_response_zero = abs(
        a019.self_derivative(
            selected.N,
            selected.rho,
            0.0,
        )
    )

    print(
        "INDEPENDENT_PAYLOAD_ACCEL_M_S2="
        f"{accel_independent:.15e}"
    )
    print(
        "INDEPENDENT_PAYLOAD_ACCEL_RELERR="
        f"{accel_relerr:.15e}"
    )
    print(
        "INDEPENDENT_C_PHI="
        f"{c_independent:.15e}"
    )
    print(
        "INDEPENDENT_C_PHI_RELERR="
        f"{c_independent_relerr:.15e}"
    )
    print(
        "INDEPENDENT_P_BACKREACTION_RATIO_MP="
        f"{p_ratio_mp:.15e}"
    )
    print(
        "INDEPENDENT_P_BACKREACTION_RELERR="
        f"{p_ratio_relerr:.15e}"
    )
    print(
        "INDEPENDENT_VECTOR_HIGGS_BETA_RATIO="
        f"{vh_ratio_independent:.15e}"
    )
    print(
        "INDEPENDENT_VECTOR_HIGGS_BETA_RELERR="
        f"{vh_ratio_relerr:.15e}"
    )
    print(
        "THETA0_LOCAL_WILSON_SELF_RESPONSE="
        f"{self_response_zero:.15e}"
    )

    independent_pass = (
        accel_relerr <= MAX_INDEPENDENT_RELERR
        and c_independent_relerr <= MAX_INDEPENDENT_RELERR
        and p_ratio_relerr <= MAX_INDEPENDENT_RELERR
        and vh_ratio_relerr <= 1.0e-4
        and self_response_zero <= 1.0e-12
    )

    print(
        "INDEPENDENT_RECONSTRUCTION="
        + ("PASS" if independent_pass else "FAIL")
    )

    # ------------------------------------------------------------------
    # H. Local neighboring perturbation robustness.
    # ------------------------------------------------------------------
    print("\n=== H — SELECTED-POINT LOCAL ROBUSTNESS ===")

    neighbor_total = 0
    neighbor_pass = 0

    lambda_factors = (0.8, 1.0, 1.2)
    rho_factors = (0.9, 1.0, 1.1)
    g_factors = (0.9, 1.0, 1.1)

    for lf in lambda_factors:
        neighbor_range = (
            geo.range_m * lf
        )

        if (
            neighbor_range < min(LAMBDA_VALUES)
            or neighbor_range > max(LAMBDA_VALUES)
        ):
            continue

        neighbor_geo = geometry_point(
            neighbor_range
        )

        for rf in rho_factors:
            rho_neighbor = (
                selected.rho * rf
            )

            if not (
                min(RHO_VALUES)
                <= rho_neighbor
                <= max(RHO_VALUES)
            ):
                continue

            # Interpolate Wilson curvature by evaluating the actual function.
            kappa_neighbor = float(
                a019.cw_curvature_analytic_mp(
                    selected.N,
                    rho_neighbor,
                )
            )

            for gf in g_factors:
                g_neighbor = (
                    selected.g_bridge * gf
                )

                neighbor_total += 1

                neighbor = portal_point(
                    a019,
                    b019,
                    neighbor_geo,
                    selected.N,
                    rho_neighbor,
                    selected.scale_margin,
                    g_neighbor,
                    kappa_neighbor,
                    bx_mix_fraction,
                    bx_mix_margin,
                )

                if (
                    neighbor is not None
                    and point_passes(neighbor)
                ):
                    neighbor_pass += 1

    neighbor_fraction = (
        neighbor_pass
        / max(neighbor_total, 1)
    )

    print(
        "LOCAL_NEIGHBOR_TOTAL="
        f"{neighbor_total}"
    )
    print(
        "LOCAL_NEIGHBOR_PASS="
        f"{neighbor_pass}"
    )
    print(
        "LOCAL_NEIGHBOR_PASS_FRACTION="
        f"{neighbor_fraction:.15e}"
    )

    local_robustness_pass = (
        neighbor_total >= 9
        and neighbor_fraction >= 0.8
    )

    print(
        "LOCAL_NEIGHBORHOOD_ROBUSTNESS="
        + (
            "PASS"
            if local_robustness_pass
            else "FAIL"
        )
    )

    # ------------------------------------------------------------------
    # Blind wildcard diagnostics.
    # ------------------------------------------------------------------
    print("\n=== BLIND WILDCARD DIAGNOSTICS — NOT EVIDENCE ===")

    for factor in BLIND_WILDCARDS:
        test_range = min(
            max(
                selected.geometry.range_m * factor,
                min(LAMBDA_VALUES),
            ),
            max(LAMBDA_VALUES),
        )

        test_geo = geometry_point(
            test_range
        )

        test_point = portal_point(
            a019,
            b019,
            test_geo,
            selected.N,
            selected.rho,
            selected.scale_margin,
            selected.g_bridge,
            selected.kappa_cw,
            bx_mix_fraction,
            bx_mix_margin,
        )

        if test_point is None:
            print(
                f"WILDCARD_FACTOR={factor:.6f} STATUS=NO_POINT"
            )
            continue

        print(
            f"WILDCARD_FACTOR={factor:.6f} "
            f"RANGE_M={test_range:.9e} "
            f"Y_P={test_point.y_p:.9e} "
            f"P_NAT={test_point.p_mass2_ratio:.9e} "
            f"VH_NAT={test_point.vector_higgs_beta_mass2_ratio:.9e} "
            f"FULL_GATE={'PASS' if point_passes(test_point) else 'FAIL'}"
        )

    print(
        "BLIND_WILDCARD_VALUES_USED_AS_EVIDENCE=NO"
    )

    # ------------------------------------------------------------------
    # I. Decision.
    # ------------------------------------------------------------------
    print("\n=== 021A DECISION ===")

    finite_payload_pass = (
        selected_is_passer
        and accel_relerr <= MAX_INDEPENDENT_RELERR
    )

    core_pass = (
        bx_anomaly_pass
        and isotope_sign_pass
        and one_body_pass
        and cw_reconstruction_pass
        and robust_basin
        and selected_is_passer
        and finite_payload_pass
        and independent_pass
        and local_robustness_pass
    )

    if core_pass:
        print(
            "021A_SHORT_RANGE_ISOTOPE_SIGN_WILSON_VECTOR_PORTAL_GATE="
            "GREEN"
        )
        print(
            "NEW_STRUCTURAL_SCALING_MECHANISM="
            "SHORT_RANGE_DUAL_ACTIVATION_PLUS_ISOTOPE_SIGN_INVERSION"
        )
        print(
            "ANOMALY_FREE_COMPOSITION_CURRENT="
            "PASS"
        )
        print(
            "OPPOSITE_SIGN_NORMAL_MATTER_SOURCE_AND_PAYLOAD="
            "PASS_IN_DECLARED_ISOTOPE_CURRENT_MODEL"
        )
        print(
            "FINITE_SOURCE_FINITE_PAYLOAD_1G="
            "PASS"
        )
        print(
            "GROUND_REACTION_MOMENTUM_ACCOUNTED="
            "YES"
        )
        print(
            "RENORMALIZABLE_LOOP_SEEDED_VECTOR_HIGGS_PORTAL="
            "PASS_AT_EXPLICIT_PARAMETER_POINT"
        )
        print(
            "WILSON_NONLOCAL_PROTECTION="
            "PASS"
        )
        print(
            "WILSON_MASS_NATURALNESS="
            "PASS"
        )
        print(
            "P_BRIDGE_BACKREACTION_NATURALNESS="
            "PASS"
        )
        print(
            "VECTOR_HIGGS_CW_RUNNING_NATURALNESS="
            "PASS"
        )
        print(
            "ALL_NEW_STATES_ABOVE_2X_MATERIAL_EFT="
            "PASS"
        )
        print(
            "BALANCED_PERTURBATIVE_BRIDGE_COUPLINGS="
            "PASS"
        )
        print(
            "BRIDGE_SCALAR_LOCAL_STABILITY="
            "PASS"
        )
        print(
            "SOURCE_WILSON_EXCURSION="
            "PASS"
        )
        print(
            "ONE_BODY_VECTOR_MIXING_PREFLIGHT="
            "PASS"
        )
        print(
            "ROBUST_PARAMETER_BASIN="
            "YES"
        )
        print(
            "COMPLETE_PROTECTED_MICROSCOPIC_PORTAL_PREFLIGHT="
            "YES_IN_DECLARED_SHORT_RANGE_MODEL"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_70_PERCENT_NOT_A_PROBABILITY"
        )
        print(
            "HEURISTIC_CHANGE="
            "APPROXIMATELY_68_TO_70_PERCENT_IF_CLAIM_AUDIT_ACCEPTS_021A"
        )
        print(
            "NEXT="
            "021B_COMPLETE_OPERATOR_MIXING_SHORT_RANGE_EXPERIMENTAL_AND_ISOTOPE_MATERIAL_GATE"
        )
    else:
        print(
            "021A_SHORT_RANGE_ISOTOPE_SIGN_WILSON_VECTOR_PORTAL_GATE="
            "GREEN_NEGATIVE_OR_INCOMPLETE_RESULT"
        )
        print(
            "COMPLETE_PROTECTED_MICROSCOPIC_PORTAL_PREFLIGHT="
            "NO"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY"
        )
        print(
            "HEURISTIC_CHANGE="
            "NONE"
        )
        print(
            "NEXT="
            "GLOBAL_RERANK_CONTINUES_DO_NOT_ENLARGE_WILSON_QUIVER"
        )

    # Permanent claim boundaries.
    print(
        "FE54_FE58_STABLE_ISOTOPES="
        "LITERATURE_FACT_NOT_PORTAL_EVIDENCE"
    )
    print(
        "DINUCLEAR_FEII_SPIN_CROSSOVER_CLASS="
        "LITERATURE_BACKED_HOST_CLASS"
    )
    print(
        "ISOTOPE_ENRICHED_SCO_PRESERVATION="
        "NOT_ESTABLISHED"
    )
    print(
        "EXACT_PRESENT_SHORT_RANGE_EXPERIMENTAL_CLOSURE="
        "NOT_YET"
    )
    print(
        "COMPLETE_ALL_ORDER_SM_OPERATOR_MIXING="
        "NOT_YET"
    )
    print(
        "STELLAR_COSMOLOGICAL_COMPLETION="
        "NOT_ESTABLISHED"
    )
    print(
        "REAL_MATERIAL_WITH_REQUIRED_PORTAL="
        "NO"
    )
    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )
    print(
        "REACTIONLESS_PROPULSION="
        "NO"
    )
    print(
        "NEW_PHYSICS_DISCOVERY="
        "NO"
    )

    # Preserve prior science.
    print(
        "006D_CONSTRUCTIVE_LINEARIZED_GR_RESULT="
        "RETAINED"
    )
    print(
        "018B_FIELD_EXISTENCE_RESULT="
        "RETAINED"
    )
    print(
        "018C_M2_STABILITY_FALSIFICATION="
        "RETAINED"
    )
    print(
        "019A_WILSON_PROTECTION_RESULT="
        "RETAINED"
    )
    print(
        "019B_VECTOR_CURRENT_RESULT="
        "RETAINED"
    )
    print(
        "019C_5KM_LOOP_SEED_FAILURE="
        "RETAINED_FOR_OLD_TARGET"
    )
    print(
        "020A2R_5KM_MINIMAL_CLASS_CLOSEOUT="
        "RETAINED_FOR_OLD_TARGET"
    )
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_021A_SHORT_RANGE_ISOTOPE_SIGN_WILSON_VECTOR_PORTAL_PROMOTION_GATE"
    )


if __name__ == "__main__":
    main()
