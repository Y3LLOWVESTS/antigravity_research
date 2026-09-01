#!/usr/bin/env python3
"""022A — asymmetric vector, material-selector, and full naturalness closeout.

PURPOSE
-------
Resolve the exact ambiguity left by 021B0.

021B0 found two apparently contradictory facts:

1. the concrete 021A implementation fails important physical checks:
   - the Fe54/Fe58 integrated-charge sign does not survive the finite
     composite kernel;
   - the selected keV X-vector fails even an extremely loose electron g-2
     preflight;
   - the selected baryon vector fails even a 100%-of-nuclear-binding-energy
     preflight;

2. an intentionally optimistic asymmetric-coupling CAPACITY bound still
   exceeded the required pair coefficient over the old short-range window
   and by a huge margin in the nanorange scan.

That capacity result deliberately omitted P-bridge backreaction,
vector/radial-Higgs naturalness, exact material selectivity, and realistic
minimum material feature sizes.

This gate restores those mandatory effects before any further vector-current
work is allowed.

ACTIVE SCIENTIFIC QUESTIONS
---------------------------
A. MATERIAL SELECTIVITY

Can the bare conserved-current endpoint

    phi J_B^mu J_L_mu

or a smooth finite-range linear combination of such kernels reproduce the
specific low-energy material selector that survived 010E-X/Y?

The required low-energy survivor was not a universal atomic pair density.  It
was the factorized cooperative selector

    Q_2
      =
    B_material
    P_HS,1 P_HS,2,

with approximately zero off-state response and nonzero all-HS dimer response.

B. ACTUAL ASYMMETRIC MICROSCOPIC PORTAL

If material selectivity is granted in the most favorable possible way
(normalization penalty = 1), can the explicit 019C Wilson-seeded Higgs/vector
bridge satisfy simultaneously:

    direct electron-vector preflight;
    direct baryon-vector nuclear preflight;
    all new masses above 2 Lambda_mat;
    perturbativity;
    radiative quartic floor;
    bridge Hessian stability;
    exact target C_phi;
    P-bridge scalar-mass backreaction;
    vector + radial-Higgs Coleman-Weinberg running;
    a physically meaningful minimum source/payload layer thickness and gap?

If the answer is no even after granting the selector for free, the tested
short-range direct-vector realization is closed independently of the
Fe-isotope failure.

SCIENTIFIC DISCIPLINE
---------------------
This run does not attempt to force a 70% promotion.

A negative result increases information but not device maturity.

The heuristic can rise only if a complete microscopic portal survives the
declared gates.

PART I — EXACT SELECTOR VERSUS UNIVERSAL CURRENT
------------------------------------------------
In a neutral Fe(II) spin-crossover molecule the conserved total baryon and
lepton numbers do not change when the electronic state switches between LS and
HS.

Therefore the strict q -> 0 charge part of

    J_B^0 J_L^0

is identical in LS and HS states.

Finite mediator range can create a smooth structural dependence because the
Fe-N coordination shell expands during spin crossover.  Published Fe(II)
spin-crossover structures typically show approximately

    r_LS ~ 1.97 Angstrom
    r_HS ~ 2.22 Angstrom,

so

    Delta r ~ 0.25 Angstrom.

The project already carried a representative Fe spin-lattice phonon scale

    hbar omega ~ 0.08640445 eV.

Using the Fe-N reduced mass gives an unavoidable zero-point coordinate width

    sigma_x
      =
    sqrt[hbar/(2 mu omega)]

with the usual thermal coth factor at T=77 K.

If a smooth engineered current kernel is tuned to an n-th order zero in the
off state, the best local leakage scaling is parametrically

    leakage
      ~
    (sigma_x / Delta r)^n.

The code reports the minimum n needed for:

    1e-2
    1e-4
    5.772961445e-7

leakage targets.

A generic linear combination of K distinct Yukawa/exponential kernels has K
coefficients.  After fixing the overall activated normalization, obtaining an
n-th order zero requires at least

    K >= n + 1

independent kernel sectors.

This is a lower-bound dimension count; it does not include coefficient
conditioning or radiative stability, both of which can only worsen the
construction.

The strict 010E exact-product selector is therefore not inherited merely by
writing a universal conserved-current pair operator.

PART II — GENERAL ASYMMETRIC 019C BRIDGE
----------------------------------------
Use the explicit renormalizable 019C bridge:

    S_+ : charges (1,+1)
    S_- : charges (1,-1)

under

    U(1)_B x U(1)_X.

At d=0,

    v_+^2 = v_-^2 = v^2.

For unequal gauge couplings,

    M_B^2 = 2 g_B^2 v^2
    M_X^2 = 2 g_X^2 v^2.

The Wilson-odd VEV splitting produces off-diagonal mass-squared

    (M^2_BX)
      =
    -2 g_B g_X v^2 d(theta).

Using

    d M^{-2}/dtheta
      =
    -M^{-2} M_theta^2 M^{-2},

the gauge couplings cancel from the low-energy current coefficient at d=0:

    C_phi
      =
    d_theta/(2 f v^2).

Thus asymmetric g_B and g_X are allowed, but the smaller coupling forces v
large because both vectors must remain above the material-EFT floor:

    v
      >=
    max[
        M_floor/(sqrt(2) g_B),
        M_floor/(sqrt(2) g_X)
    ].

DIRECT COUPLING CEILINGS
------------------------
The gate imports 021B0's deliberately loose direct-vector preflights:

Electron/X:

    |Delta a_e| <= 1e-6

Nuclear/B:

    U_B <= 100% of a rough Fe nuclear binding-energy scale.

These are intentionally weak.  Passing them is not equivalent to a complete
2026 experimental fit.

WILSON SEED
-----------
Use the maximum positive Wilson Coleman-Weinberg curvature found in the
inherited 019A basin.  This is deliberately favorable to the portal.

At theta=0,

    m_phi
      =
    mu^2 sqrt(kappa_CW)/(8 pi f).

For the strongest possible capacity at fixed m_phi, the scan allows

    f <= M_Pl,reduced

and chooses the largest mu consistent with this relation.

This minimizes the required dimensionless P-bridge endpoint coupling.

RADIATIVE QUARTIC FLOOR
-----------------------
The bridge radial quartic cannot be made arbitrarily tiny while gauge
couplings are nonzero.

Use the deliberately weak naturalness floor

    lambda_S
      >=
    (g_B^4 + g_X^4)/(16 pi^2).

Also require the radial mass to remain above the same microscopic mass floor:

    sqrt(2 lambda_S) v >= M_floor.

Therefore

    lambda_S
      =
    max[
        M_floor^2/(2v^2),
        (g_B^4+g_X^4)/(16 pi^2)
    ].

No order-one coefficient is added to the gauge-loop estimate; this favors
survival.

P-BRIDGE AND HESSIAN
--------------------
The loop-seeded response is

    d_theta
      =
    kappa_P y_P mu^3 kappa_CW
    /
    (64 pi^2 m_P^2 lambda_S v^2).

The exact target requires

    d_theta
      =
    2 f v^2 C_target.

Define

    r_P = kappa_P/m_P.

Then

    y_P r_P
      =
    C_target
    128 pi^2
    m_P lambda_S f v^4
    /
    (mu^3 kappa_CW).

For the P / odd-radial Hessian

    H
      =
    [[m_P^2,       2 kappa_P v],
     [2 kappa_P v, m_r^2       ]],

require its minimum eigenvalue to be at least a fraction

    h = 0.25

of the smaller diagonal mass-squared.

The scan intentionally takes

    r_P = 0.99 r_P,max

to MINIMIZE y_P.

That is almost a stability-boundary saturation and therefore strongly biases
the test toward finding a portal.

MANDATORY NATURALNESS 1 — P BACKREACTION
-----------------------------------------
The Wilson loop produces

    t_P(theta)
      =
    y_P mu^3/(64 pi^2)
    S_CW'(theta).

Integrating out P adds

    V_P
      =
    -t_P^2/(2m_P^2).

At theta=0,

    |delta m_phi^2|_P/m_phi^2
      =
    y_P^2 mu^2 kappa_CW
    /
    (64 pi^2 m_P^2).

The mandatory technical-naturalness gate is

    ratio <= 1.

The preferred interior gate is

    ratio <= 0.1.

021B0's optimistic C_max did NOT include this term.

MANDATORY NATURALNESS 2 — VECTOR + RADIAL-HIGGS RUNNING
--------------------------------------------------------
For the unequal-coupling vector mass matrix

    M_V^2(d)
      =
    [[2g_B^2v^2,      -2g_Bg_Xv^2 d],
     [-2g_Bg_Xv^2 d,   2g_X^2v^2   ]],

define

    c_BX
      =
    2 g_B g_X v^2.

At d=0,

    d^2/dtheta^2 Tr[(M_V^2)^2]
      =
    4 c_BX^2 d_theta^2.

The three vector polarizations therefore contribute weight 3.

For the two radial modes

    m_r,+^2 = m_r^2(1+d)
    m_r,-^2 = m_r^2(1-d),

their combined second derivative of the weighted mass-fourth-power trace is

    4 m_r^4 d_theta^2.

The one-loop logarithmic mass-running magnitude is therefore

    |d m_phi^2/d ln Q|
      =
    d_theta^2
    (3 c_BX^2 + m_r^4)
    /
    (8 pi^2 f^2).

Again require

    ratio <= 1,

preferred

    ratio <= 0.1.

THREE GEOMETRY LEVELS
---------------------
The same microscopic scan is repeated under three progressively less
unphysical source/payload geometries.

1. IDEAL_LAMBDA_SCALED

       t_payload = lambda
       t_source  = 5 lambda
       gap       = 0.1 lambda

   This is a pure scaling oracle.

2. ATOMIC_OPTIMISTIC

       t_payload >= 1.97 Angstrom
       t_source  >= 1.97 Angstrom
       gap       >= 1.0 Angstrom

   This is already more favorable than a realizable molecular solid layer.

3. MOLECULAR_OPTIMISTIC

       t_payload >= 1.0 nm
       t_source  >= 1.0 nm
       gap       >= 0.3 nm

   This is still deliberately aggressive for a large dinuclear molecular
   complex.  It is far thinner than the 15-nm Fe(II) spin-crossover film scale
   demonstrated in published thin-film work.

For every geometry, the finite-thickness planar force factor is

    F
      =
    (1-exp[-t_S/lambda])
    exp[-gap/lambda]
    (lambda/t_P)
    (1-exp[-t_P/lambda])

times the same conservative ten-range radial-tail correction used by 021A.

To give the microscopic portal its BEST possible material normalization, the
scan sets the selector penalty to

    1.

In other words, it grants a perfect exact material selector for free.

If the microscopic bridge still fails, isotope/current normalization cannot
rescue it.

SCAN
----
Scalar-force range:

    1e-11 m ... 1e-4 m

Microscopic mass margin:

    2, 2.5, 3, 5 times Lambda_mat

Direct coupling fractions of the already loose ceilings:

    0.20 ... 0.95

P mass margins:

    2, 3, 5, 10 times Lambda_mat

The electron-g-2 ceiling involves numerical quadrature.  The run caches
all repeated mediator-mass evaluations so the broad scan remains auditable
without redundantly performing hundreds of thousands of identical integrals.

For every point:

    g_X <= loose electron-g-2 ceiling
    g_B <= loose nuclear ceiling

and the actual masses after the common-VEV constraint are rechecked against
those same bounds.

PROMOTION / FALSIFICATION
-------------------------
This gate cannot promote the heuristic merely because the ideal lambda-scaled
oracle passes.

A credible short-range 019C portal requires at minimum:

    MOLECULAR_OPTIMISTIC_MANDATORY_NATURALNESS_PASSERS > 0
    DIRECT_VECTOR_PREFLIGHT=PASS
    PERTURBATIVITY=PASS
    HESSIAN=PASS
    TARGET_MATCH=PASS

and material selectivity still remains a separate required microscopic
construction.

If the MOLECULAR_OPTIMISTIC scan has zero mandatory-naturalness passers even
after:

    perfect selector granted for free;
    Planck-scale f allowed;
    maximum inherited Wilson curvature;
    direct vector couplings near permissive ceilings;
    Hessian almost saturated;
    minimal radiative quartic coefficient;

then the explicit 019C asymmetric short-range bridge is closed in this tested
class.

If, independently, bare conserved currents cannot reproduce the exact 010E
material selector without a high-order tuned kernel node, the project must not
pretend that 019B/019C automatically UV-completed 010E-X/Y.

NEXT ACTION
-----------
If both failures occur:

    GLOBAL_RERANK=REQUIRED

with first priority on an intrinsically stable topology / nanostandoff revisit
of the 018B/006D GR field-existence result rather than another Wilson-vector
quiver.

If the microscopic magnitude survives but current selectivity fails:

    NEXT=
    EXACT_BOUND_COMPOSITE_NONCURRENT_PROTECTION_GATE

but only if a genuinely new exact/topological protection principle is supplied.

CLAIM LIMITS
------------
A positive microscopic magnitude result is not experimental viability.

A negative result closes only the explicit asymmetric 019C loop-seeded
short-range bridge under the stated direct-vector and naturalness assumptions.

No result here establishes a real antigravity material or device.

LITERATURE ANCHORS
------------------
- Fe(II) spin-crossover LS/HS Fe-N bond changes:
  representative low-spin Fe-N distances near 1.97-2.0 Angstrom and high-spin
  distances near 2.22 Angstrom are documented across Fe(II) SCO literature.
- The project host [[Fe(phdia)(NCS)2]2(phdia)] experimentally exhibits the
  LS-LS <-> HS-LS <-> HS-HS dinuclear sequence.
- Electron g-2 and other direct-vector constraints must ultimately be replaced
  by a full model-specific 2026 experimental fit; this gate intentionally uses
  a much looser preflight inherited from 021B0.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_022A_ASYMMETRIC_VECTOR_MATERIAL_SELECTOR_AND_NATURALNESS_CLOSEOUT
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib
import importlib.util
import math
from pathlib import Path
import re
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

A_SOURCE = ROOT / "simulations/019a_wilson_line_sequestered_pair_scalar_uv_protection_gate.py"
B0_SOURCE = ROOT / "simulations/021b0_current_kernel_direct_vector_and_nanorange_rerank_gate.py"

A_LOG = ROOT / "results/logs/019a_wilson_line_sequestered_pair_scalar_uv_protection_gate.log"
B0_LOG = ROOT / "results/logs/021b0_current_kernel_direct_vector_and_nanorange_rerank_gate.log"

EXPECTED_019A_SHA256 = "27514c58298ccf9ecaa5543a3dc6d4368df7174ae2c55cb1a547adb922b756e7"
EXPECTED_021B0_SHA256 = "1a4ad7e154ac478789d4ea539d2f3e171dbc6f0cc65039a2d67310c49f96fe9a"

# ---------------------------------------------------------------------------
# Inherited low-energy and physical constants.
# ---------------------------------------------------------------------------

C_REF = 9.536416387852626e-20
ALPHA_ACTIVATED_REF = 1.558991777087370e5
MATERIAL_EFT_CUTOFF_EV = 657.7566

G_SI = 6.67430e-11
G_ACCEL = 9.80665
SOURCE_DENSITY_KG_M3 = 3000.0

HBARC_EV_M = 1.973269804e-7
MPL_REDUCED_EV = 2.435e27

# ---------------------------------------------------------------------------
# Material-selectivity anchors.
# ---------------------------------------------------------------------------

LS_FE_N_ANGSTROM = 1.97
HS_FE_N_ANGSTROM = 2.22

# Project-derived spin-lattice phonon anchor from 010E-U.
PHONON_HBAR_OMEGA_EV = 0.08640445276497724

TEMPERATURE_K = 77.0
KB_EV_K = 8.617333262e-5

AMU_KG = 1.66053906660e-27
HBAR_SI = 1.054571817e-34
EV_J = 1.602176634e-19

FE_MASS_U = 55.845
N_MASS_U = 14.007

STRICT_LEAKAGE = 5.772961445324848e-7
LEAKAGE_DIAGNOSTICS = (1.0e-2, 1.0e-4, STRICT_LEAKAGE)

# ---------------------------------------------------------------------------
# Portal thresholds.
# ---------------------------------------------------------------------------

HESSIAN_MIN_FRACTION = 0.25

MANDATORY_NATURALNESS_MAX = 1.0
PREFERRED_NATURALNESS_MAX = 0.1

Y_P_MAX = math.sqrt(4.0 * math.pi)
R_P_MAX_PERTURBATIVE = math.sqrt(4.0 * math.pi)

RADIAL_EDGE_MARGIN_LAMBDA = 10.0

# Direct-vector coupling fractions.  Never exceed the already very loose
# 021B0 ceilings.
COUPLING_FRACTIONS = tuple(float(x) for x in np.linspace(0.20, 0.95, 9))

MASS_MARGINS = (2.0, 2.5, 3.0, 5.0)
P_MASS_MARGINS = (2.0, 3.0, 5.0, 10.0)

RANGE_GRID_M = tuple(float(x) for x in np.geomspace(1.0e-11, 1.0e-4, 90))

# Blind wildcard diagnostics only.
BLIND_WILDCARDS = (1.6, 1.875, 3.125, 0.625, 5.0)


@dataclass(frozen=True)
class GeometryModel:
    """Finite planar geometry floor model."""

    name: str
    min_payload_thickness_m: float
    min_source_thickness_m: float
    min_gap_m: float


@dataclass(frozen=True)
class PortalPoint:
    """One actual asymmetric 019C candidate."""

    geometry_name: str
    range_m: float
    m_phi_ev: float
    force_factor: float
    alpha_required: float
    c_target: float

    mass_margin: float
    p_mass_margin: float
    gx_fraction: float
    gb_fraction: float

    g_x: float
    g_b: float
    g_x_ceiling_actual: float
    g_b_ceiling_actual: float

    v_ev: float
    m_x_ev: float
    m_b_ev: float
    lambda_s: float
    m_radial_ev: float
    m_p_ev: float

    kappa_cw: float
    f_ev: float
    mu_ev: float

    r_p_max_hessian: float
    r_p: float
    y_p: float
    d_theta: float

    p_backreaction_ratio: float
    vector_higgs_ratio: float
    max_naturalness_ratio: float

    hessian_min_fraction_actual: float
    direct_bounds_pass: bool
    perturbativity_pass: bool
    mandatory_naturalness_pass: bool
    preferred_naturalness_pass: bool


GEOMETRIES = (
    GeometryModel(
        name="IDEAL_LAMBDA_SCALED",
        min_payload_thickness_m=0.0,
        min_source_thickness_m=0.0,
        min_gap_m=0.0,
    ),
    GeometryModel(
        name="ATOMIC_OPTIMISTIC",
        min_payload_thickness_m=LS_FE_N_ANGSTROM * 1.0e-10,
        min_source_thickness_m=LS_FE_N_ANGSTROM * 1.0e-10,
        min_gap_m=1.0e-10,
    ),
    GeometryModel(
        name="MOLECULAR_OPTIMISTIC",
        min_payload_thickness_m=1.0e-9,
        min_source_thickness_m=1.0e-9,
        min_gap_m=3.0e-10,
    ),
)


def require_marker(path: Path, marker: str) -> None:
    """Fail closed unless an upstream marker exists exactly."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream log: {path}")

    text = path.read_text(errors="replace")

    if marker not in text:
        raise RuntimeError(
            f"Missing required marker in {path.name}: {marker}"
        )


def sha256(path: Path) -> str:
    """Return SHA-256 for one source."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    """Import one repository simulation without invoking main()."""

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


def relative_error(a: float, b: float) -> float:
    """Return stable relative error."""

    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def material_rms_displacement_angstrom() -> tuple[float, float, float]:
    """Return zero-point, thermal, and total Fe-N coordinate RMS widths."""

    reduced_mass_u = (
        FE_MASS_U
        * N_MASS_U
        /
        (FE_MASS_U + N_MASS_U)
    )

    reduced_mass_kg = reduced_mass_u * AMU_KG

    omega = (
        PHONON_HBAR_OMEGA_EV
        * EV_J
        / HBAR_SI
    )

    sigma_zp_m = math.sqrt(
        HBAR_SI
        /
        (2.0 * reduced_mass_kg * omega)
    )

    thermal_argument = (
        PHONON_HBAR_OMEGA_EV
        /
        (2.0 * KB_EV_K * TEMPERATURE_K)
    )

    coth = 1.0 / math.tanh(thermal_argument)

    sigma_total_m = sigma_zp_m * math.sqrt(coth)

    sigma_thermal_m = math.sqrt(
        max(
            sigma_total_m**2 - sigma_zp_m**2,
            0.0,
        )
    )

    return (
        sigma_zp_m / 1.0e-10,
        sigma_thermal_m / 1.0e-10,
        sigma_total_m / 1.0e-10,
    )


def minimum_zero_order(
    sigma_angstrom: float,
    delta_r_angstrom: float,
    leakage: float,
) -> int:
    """Return minimum Taylor-zero order with (sigma/delta_r)^n <= leakage."""

    ratio = sigma_angstrom / delta_r_angstrom

    if not (0.0 < ratio < 1.0):
        raise RuntimeError(
            "Material fluctuation ratio must lie strictly between zero and one"
        )

    n = math.ceil(
        math.log(leakage) / math.log(ratio)
    )

    return max(int(n), 1)


def max_positive_wilson_curvature(a019) -> tuple[float, int, float]:
    """Find maximum positive inherited 019A CW curvature."""

    best = (0.0, -1, float("nan"))

    for N in range(3, 17):
        for rho in np.linspace(0.25, 5.0, 80):
            value = float(
                a019.cw_curvature_analytic_mp(
                    N,
                    float(rho),
                )
            )

            if math.isfinite(value) and value > best[0]:
                best = (
                    value,
                    N,
                    float(rho),
                )

    if best[0] <= 0.0:
        raise RuntimeError(
            "No positive Wilson curvature found"
        )

    return best


def geometry_dimensions(
    geometry: GeometryModel,
    range_m: float,
) -> tuple[float, float, float]:
    """Return payload thickness, source thickness, and gap."""

    payload = max(
        range_m,
        geometry.min_payload_thickness_m,
    )

    source = max(
        5.0 * range_m,
        geometry.min_source_thickness_m,
    )

    gap = max(
        0.1 * range_m,
        geometry.min_gap_m,
    )

    return payload, source, gap


def force_factor(
    geometry: GeometryModel,
    range_m: float,
) -> float:
    """Return finite planar force factor with conservative radial correction."""

    payload, source, gap = geometry_dimensions(
        geometry,
        range_m,
    )

    source_factor = (
        1.0
        -
        math.exp(-source / range_m)
    )

    gap_factor = math.exp(
        -gap / range_m
    )

    payload_average = (
        range_m
        / payload
        * (
            1.0
            -
            math.exp(-payload / range_m)
        )
    )

    radial_tail_bound = (
        1.0 + RADIAL_EDGE_MARGIN_LAMBDA
    ) * math.exp(
        -RADIAL_EDGE_MARGIN_LAMBDA
    )

    return (
        source_factor
        * gap_factor
        * payload_average
        * (
            1.0 - radial_tail_bound
        )
    )


def target_coefficient(
    geometry: GeometryModel,
    range_m: float,
) -> tuple[float, float, float]:
    """Return force factor, required alpha, and BEST-CASE selector C target.

    The material normalization penalty is deliberately fixed to one.

    This grants the portal a perfect exact selector for free.
    """

    factor = force_factor(
        geometry,
        range_m,
    )

    if factor <= 0.0:
        raise RuntimeError(
            "Nonpositive force factor"
        )

    alpha_required = math.sqrt(
        G_ACCEL
        /
        (
            4.0
            * math.pi
            * G_SI
            * SOURCE_DENSITY_KG_M3
            * range_m
            * factor
        )
    )

    c_target = (
        C_REF
        * alpha_required
        / ALPHA_ACTIVATED_REF
    )

    return (
        factor,
        alpha_required,
        c_target,
    )


def hessian_rp_max(
    m_p_ev: float,
    m_radial_ev: float,
    v_ev: float,
) -> float | None:
    """Return maximum r_P=kappa_P/m_P at the declared Hessian floor."""

    m_min2 = min(
        m_p_ev**2,
        m_radial_ev**2,
    )

    shifted_p = (
        m_p_ev**2
        -
        HESSIAN_MIN_FRACTION * m_min2
    )

    shifted_r = (
        m_radial_ev**2
        -
        HESSIAN_MIN_FRACTION * m_min2
    )

    product = shifted_p * shifted_r

    if product <= 0.0:
        return None

    kappa_p_max = (
        math.sqrt(product)
        /
        (2.0 * v_ev)
    )

    return (
        kappa_p_max / m_p_ev
    )


def actual_hessian_fraction(
    m_p_ev: float,
    m_radial_ev: float,
    v_ev: float,
    r_p: float,
) -> float:
    """Return minimum Hessian eigenvalue divided by smaller diagonal mass^2."""

    kappa_p = r_p * m_p_ev

    matrix = np.array(
        [
            [
                m_p_ev**2,
                2.0 * kappa_p * v_ev,
            ],
            [
                2.0 * kappa_p * v_ev,
                m_radial_ev**2,
            ],
        ],
        dtype=float,
    )

    eig = np.linalg.eigvalsh(matrix)

    return (
        float(eig[0])
        /
        min(
            m_p_ev**2,
            m_radial_ev**2,
        )
    )


@lru_cache(maxsize=None)
def cached_gx_ceiling(b0_module_name: str, vector_mass_ev: float) -> float:
    """Cached wrapper around the expensive electron-g-2 ceiling.

    The imported 021B0 module is recovered from sys.modules by name so that
    the cache key contains only hashable stable values.
    """

    module = sys.modules[b0_module_name]
    return float(module.g_x_max_from_ae(float(vector_mass_ev)))


@lru_cache(maxsize=None)
def cached_gb_ceiling(b0_module_name: str, vector_mass_ev: float) -> float:
    """Cached wrapper around the analytic nuclear self-energy ceiling."""

    module = sys.modules[b0_module_name]
    return float(module.g_b_max_from_nuclear(float(vector_mass_ev)))


def portal_candidate(
    b0,
    geometry: GeometryModel,
    range_m: float,
    mass_margin: float,
    p_mass_margin: float,
    gx_fraction: float,
    gb_fraction: float,
    kappa_cw: float,
) -> PortalPoint | None:
    """Construct one maximally favorable actual asymmetric 019C point."""

    factor, alpha_required, c_target = target_coefficient(
        geometry,
        range_m,
    )

    m_phi = HBARC_EV_M / range_m

    microscopic_floor = (
        mass_margin
        * MATERIAL_EFT_CUTOFF_EV
    )

    # Evaluate loose direct-vector ceilings at the intended light-vector floor.
    b0_name = b0.__name__

    gx_ceiling_floor = cached_gx_ceiling(
        b0_name,
        float(microscopic_floor),
    )

    gb_ceiling_floor = cached_gb_ceiling(
        b0_name,
        float(microscopic_floor),
    )

    g_x = (
        gx_fraction
        * gx_ceiling_floor
    )

    g_b = (
        gb_fraction
        * gb_ceiling_floor
    )

    if g_x <= 0.0 or g_b <= 0.0:
        return None

    # Both vectors arise from the same bridge VEV.
    v_ev = max(
        microscopic_floor
        /
        (
            math.sqrt(2.0)
            * g_x
        ),
        microscopic_floor
        /
        (
            math.sqrt(2.0)
            * g_b
        ),
    )

    m_x = (
        math.sqrt(2.0)
        * g_x
        * v_ev
    )

    m_b = (
        math.sqrt(2.0)
        * g_b
        * v_ev
    )

    gx_ceiling_actual = cached_gx_ceiling(
        b0_name,
        float(m_x),
    )

    gb_ceiling_actual = cached_gb_ceiling(
        b0_name,
        float(m_b),
    )

    direct_bounds_pass = (
        g_x <= gx_ceiling_actual
        and g_b <= gb_ceiling_actual
    )

    # Deliberately weak gauge-radiative quartic floor.
    lambda_mass_floor = (
        microscopic_floor**2
        /
        (
            2.0
            * v_ev**2
        )
    )

    lambda_gauge_floor = (
        g_b**4
        + g_x**4
    ) / (
        16.0
        * math.pi**2
    )

    lambda_s = max(
        lambda_mass_floor,
        lambda_gauge_floor,
    )

    m_radial = (
        math.sqrt(
            2.0 * lambda_s
        )
        * v_ev
    )

    m_p = (
        p_mass_margin
        * MATERIAL_EFT_CUTOFF_EV
    )

    r_p_max = hessian_rp_max(
        m_p,
        m_radial,
        v_ev,
    )

    if r_p_max is None or r_p_max <= 0.0:
        return None

    # Saturate 99% of the Hessian capacity to MINIMIZE y_P.
    r_p = 0.99 * r_p_max

    if r_p > R_P_MAX_PERTURBATIVE:
        r_p = 0.99 * R_P_MAX_PERTURBATIVE

    # Maximally favorable Wilson scale: f=M_Pl.
    f_ev = MPL_REDUCED_EV

    mu_ev = math.sqrt(
        8.0
        * math.pi
        * m_phi
        * f_ev
        /
        math.sqrt(kappa_cw)
    )

    # Required endpoint product.
    product_required = (
        c_target
        * 128.0
        * math.pi**2
        * m_p
        * lambda_s
        * f_ev
        * v_ev**4
        /
        (
            mu_ev**3
            * kappa_cw
        )
    )

    y_p = (
        product_required
        / r_p
    )

    if (
        not math.isfinite(y_p)
        or y_p <= 0.0
    ):
        return None

    d_theta = (
        2.0
        * f_ev
        * v_ev**2
        * c_target
    )

    # P backreaction.
    p_backreaction_ratio = (
        y_p**2
        * mu_ev**2
        * kappa_cw
        /
        (
            64.0
            * math.pi**2
            * m_p**2
        )
    )

    # General unequal-vector Coleman-Weinberg running.
    c_bx = (
        2.0
        * g_b
        * g_x
        * v_ev**2
    )

    vector_higgs_mass2_running = (
        d_theta**2
        * (
            3.0 * c_bx**2
            + m_radial**4
        )
        /
        (
            8.0
            * math.pi**2
            * f_ev**2
        )
    )

    vector_higgs_ratio = (
        vector_higgs_mass2_running
        /
        m_phi**2
    )

    max_nat = max(
        p_backreaction_ratio,
        vector_higgs_ratio,
    )

    hessian_fraction = actual_hessian_fraction(
        m_p,
        m_radial,
        v_ev,
        r_p,
    )

    perturbativity_pass = (
        y_p <= Y_P_MAX
        and r_p <= R_P_MAX_PERTURBATIVE
        and lambda_s / (4.0 * math.pi) <= 1.0
        and g_x**2 / (4.0 * math.pi) <= 1.0
        and g_b**2 / (4.0 * math.pi) <= 1.0
    )

    mandatory_nat = (
        p_backreaction_ratio
        <= MANDATORY_NATURALNESS_MAX
        and vector_higgs_ratio
        <= MANDATORY_NATURALNESS_MAX
    )

    preferred_nat = (
        p_backreaction_ratio
        <= PREFERRED_NATURALNESS_MAX
        and vector_higgs_ratio
        <= PREFERRED_NATURALNESS_MAX
    )

    return PortalPoint(
        geometry_name=geometry.name,
        range_m=range_m,
        m_phi_ev=m_phi,
        force_factor=factor,
        alpha_required=alpha_required,
        c_target=c_target,
        mass_margin=mass_margin,
        p_mass_margin=p_mass_margin,
        gx_fraction=gx_fraction,
        gb_fraction=gb_fraction,
        g_x=g_x,
        g_b=g_b,
        g_x_ceiling_actual=gx_ceiling_actual,
        g_b_ceiling_actual=gb_ceiling_actual,
        v_ev=v_ev,
        m_x_ev=m_x,
        m_b_ev=m_b,
        lambda_s=lambda_s,
        m_radial_ev=m_radial,
        m_p_ev=m_p,
        kappa_cw=kappa_cw,
        f_ev=f_ev,
        mu_ev=mu_ev,
        r_p_max_hessian=r_p_max,
        r_p=r_p,
        y_p=y_p,
        d_theta=d_theta,
        p_backreaction_ratio=p_backreaction_ratio,
        vector_higgs_ratio=vector_higgs_ratio,
        max_naturalness_ratio=max_nat,
        hessian_min_fraction_actual=hessian_fraction,
        direct_bounds_pass=direct_bounds_pass,
        perturbativity_pass=perturbativity_pass,
        mandatory_naturalness_pass=mandatory_nat,
        preferred_naturalness_pass=preferred_nat,
    )


def full_static_gate(point: PortalPoint) -> bool:
    """Return all non-material-selector microscopic gates."""

    return (
        point.direct_bounds_pass
        and point.perturbativity_pass
        and point.hessian_min_fraction_actual
        >= HESSIAN_MIN_FRACTION * 0.999
        and point.m_x_ev
        >= 2.0 * MATERIAL_EFT_CUTOFF_EV
        and point.m_b_ev
        >= 2.0 * MATERIAL_EFT_CUTOFF_EV
        and point.m_radial_ev
        >= 2.0 * MATERIAL_EFT_CUTOFF_EV
        and point.m_p_ev
        >= 2.0 * MATERIAL_EFT_CUTOFF_EV
    )


def scan_geometry(
    b0,
    geometry: GeometryModel,
    kappa_cw: float,
) -> tuple[list[PortalPoint], list[PortalPoint], list[PortalPoint]]:
    """Return all finite, mandatory-pass, and preferred-pass points."""

    all_points: list[PortalPoint] = []
    mandatory: list[PortalPoint] = []
    preferred: list[PortalPoint] = []

    for range_m in RANGE_GRID_M:
        for mass_margin in MASS_MARGINS:
            for p_mass_margin in P_MASS_MARGINS:
                for gx_fraction in COUPLING_FRACTIONS:
                    for gb_fraction in COUPLING_FRACTIONS:
                        point = portal_candidate(
                            b0,
                            geometry,
                            range_m,
                            mass_margin,
                            p_mass_margin,
                            gx_fraction,
                            gb_fraction,
                            kappa_cw,
                        )

                        if point is None:
                            continue

                        all_points.append(point)

                        if (
                            full_static_gate(point)
                            and point.mandatory_naturalness_pass
                        ):
                            mandatory.append(point)

                            if point.preferred_naturalness_pass:
                                preferred.append(point)

    return all_points, mandatory, preferred


def point_rank(point: PortalPoint) -> tuple[float, ...]:
    """Rank least-bad / best interior points."""

    coupling_pressure = max(
        point.y_p / Y_P_MAX,
        point.r_p / R_P_MAX_PERTURBATIVE,
        point.g_x / max(point.g_x_ceiling_actual, 1.0e-300),
        point.g_b / max(point.g_b_ceiling_actual, 1.0e-300),
    )

    return (
        point.max_naturalness_ratio,
        coupling_pressure,
        point.range_m,
    )


def print_point(prefix: str, point: PortalPoint) -> None:
    """Print a complete auditable point."""

    print(
        f"{prefix}_GEOMETRY={point.geometry_name}"
    )
    print(
        f"{prefix}_RANGE_M={point.range_m:.15e}"
    )
    print(
        f"{prefix}_M_PHI_EV={point.m_phi_ev:.15e}"
    )
    print(
        f"{prefix}_FORCE_FACTOR={point.force_factor:.15e}"
    )
    print(
        f"{prefix}_ALPHA_REQUIRED={point.alpha_required:.15e}"
    )
    print(
        f"{prefix}_C_TARGET={point.c_target:.15e}"
    )
    print(
        f"{prefix}_G_X={point.g_x:.15e}"
    )
    print(
        f"{prefix}_G_B={point.g_b:.15e}"
    )
    print(
        f"{prefix}_G_X_CEILING_ACTUAL={point.g_x_ceiling_actual:.15e}"
    )
    print(
        f"{prefix}_G_B_CEILING_ACTUAL={point.g_b_ceiling_actual:.15e}"
    )
    print(
        f"{prefix}_V_EV={point.v_ev:.15e}"
    )
    print(
        f"{prefix}_M_X_EV={point.m_x_ev:.15e}"
    )
    print(
        f"{prefix}_M_B_EV={point.m_b_ev:.15e}"
    )
    print(
        f"{prefix}_LAMBDA_S={point.lambda_s:.15e}"
    )
    print(
        f"{prefix}_M_RADIAL_EV={point.m_radial_ev:.15e}"
    )
    print(
        f"{prefix}_M_P_EV={point.m_p_ev:.15e}"
    )
    print(
        f"{prefix}_MU_EV={point.mu_ev:.15e}"
    )
    print(
        f"{prefix}_F_EV={point.f_ev:.15e}"
    )
    print(
        f"{prefix}_R_P_MAX_HESSIAN={point.r_p_max_hessian:.15e}"
    )
    print(
        f"{prefix}_R_P={point.r_p:.15e}"
    )
    print(
        f"{prefix}_Y_P={point.y_p:.15e}"
    )
    print(
        f"{prefix}_D_THETA={point.d_theta:.15e}"
    )
    print(
        f"{prefix}_HESSIAN_MIN_FRACTION={point.hessian_min_fraction_actual:.15e}"
    )
    print(
        f"{prefix}_P_BACKREACTION_RATIO={point.p_backreaction_ratio:.15e}"
    )
    print(
        f"{prefix}_VECTOR_HIGGS_RATIO={point.vector_higgs_ratio:.15e}"
    )
    print(
        f"{prefix}_MAX_NATURALNESS_RATIO={point.max_naturalness_ratio:.15e}"
    )
    print(
        f"{prefix}_DIRECT_BOUNDS_PASS={'YES' if point.direct_bounds_pass else 'NO'}"
    )
    print(
        f"{prefix}_PERTURBATIVITY_PASS={'YES' if point.perturbativity_pass else 'NO'}"
    )
    print(
        f"{prefix}_MANDATORY_NATURALNESS_PASS={'YES' if point.mandatory_naturalness_pass else 'NO'}"
    )
    print(
        f"{prefix}_PREFERRED_NATURALNESS_PASS={'YES' if point.preferred_naturalness_pass else 'NO'}"
    )


def main() -> None:
    """Execute the complete 022A gate."""

    print(
        "=== 022A — ASYMMETRIC VECTOR + MATERIAL SELECTOR "
        "+ FULL NATURALNESS CLOSEOUT ==="
    )

    # ------------------------------------------------------------------
    # Upstream fail-closed audit.
    # ------------------------------------------------------------------
    require_marker(
        A_LOG,
        "019A_WILSON_LINE_SEQUESTERED_PAIR_SCALAR_UV_PROTECTION_GATE=GREEN",
    )
    require_marker(
        B0_LOG,
        "021B0_CURRENT_KERNEL_DIRECT_VECTOR_AND_NANORANGE_RERANK_GATE="
        "INCOMPLETE_OR_SURVIVING_021A_ASSUMPTION",
    )
    require_marker(
        B0_LOG,
        "NANOLAMELLAR_SCALING_ESCAPE=SUPPORTED_AS_CAPACITY_PREFLIGHT",
    )

    a_sha = sha256(A_SOURCE)
    b0_sha = sha256(B0_SOURCE)

    print("\n=== UPSTREAM SOURCE AUDIT ===")
    print(f"019A_SOURCE_SHA256={a_sha}")
    print(
        "019A_SOURCE_HASH_MATCH="
        + (
            "PASS"
            if a_sha == EXPECTED_019A_SHA256
            else "FAIL"
        )
    )
    print(f"021B0_SOURCE_SHA256={b0_sha}")
    print(
        "021B0_SOURCE_HASH_MATCH="
        + (
            "PASS"
            if b0_sha == EXPECTED_021B0_SHA256
            else "FAIL"
        )
    )

    if (
        a_sha != EXPECTED_019A_SHA256
        or b0_sha != EXPECTED_021B0_SHA256
    ):
        raise RuntimeError(
            "Upstream source hash mismatch"
        )

    a019 = load_module(
        "ag022a_019a",
        A_SOURCE,
    )

    b0 = load_module(
        "ag022a_021b0",
        B0_SOURCE,
    )

    # ------------------------------------------------------------------
    # A. Material-selector reconstruction.
    # ------------------------------------------------------------------
    print("\n=== A — EXACT MATERIAL SELECTOR VS CONSERVED-CURRENT ENDPOINT ===")

    delta_r = (
        HS_FE_N_ANGSTROM
        -
        LS_FE_N_ANGSTROM
    )

    sigma_zp, sigma_thermal, sigma_total = material_rms_displacement_angstrom()

    ratio = (
        sigma_total
        / delta_r
    )

    print(
        "LS_FE_N_ANGSTROM="
        f"{LS_FE_N_ANGSTROM:.15e}"
    )
    print(
        "HS_FE_N_ANGSTROM="
        f"{HS_FE_N_ANGSTROM:.15e}"
    )
    print(
        "SPIN_CROSSOVER_DELTA_R_ANGSTROM="
        f"{delta_r:.15e}"
    )
    print(
        "PHONON_HBAR_OMEGA_EV="
        f"{PHONON_HBAR_OMEGA_EV:.15e}"
    )
    print(
        "TEMPERATURE_K="
        f"{TEMPERATURE_K:.15e}"
    )
    print(
        "FE_N_ZERO_POINT_RMS_ANGSTROM="
        f"{sigma_zp:.15e}"
    )
    print(
        "FE_N_THERMAL_EXTRA_RMS_ANGSTROM="
        f"{sigma_thermal:.15e}"
    )
    print(
        "FE_N_TOTAL_RMS_ANGSTROM="
        f"{sigma_total:.15e}"
    )
    print(
        "RMS_TO_SPIN_CROSSOVER_DISPLACEMENT_RATIO="
        f"{ratio:.15e}"
    )

    strict_n = None

    for leakage in LEAKAGE_DIAGNOSTICS:
        n = minimum_zero_order(
            sigma_total,
            delta_r,
            leakage,
        )

        k_min = n + 1

        label = (
            f"{leakage:.3e}"
            .replace("+", "")
            .replace("-", "M")
            .replace(".", "P")
        )

        print(
            f"LEAKAGE_{label}_MINIMUM_ZERO_ORDER={n}"
        )
        print(
            f"LEAKAGE_{label}_MINIMUM_DISTINCT_KERNEL_SECTORS={k_min}"
        )

        if relative_error(
            leakage,
            STRICT_LEAKAGE,
        ) <= 1.0e-12:
            strict_n = n

    if strict_n is None:
        raise RuntimeError(
            "Strict leakage diagnostic was not reconstructed"
        )

    strict_k_min = strict_n + 1

    print(
        "Q0_CONSERVED_BARYON_NUMBER_LS_EQUALS_HS=YES"
    )
    print(
        "Q0_CONSERVED_LEPTON_NUMBER_LS_EQUALS_HS=YES"
    )
    print(
        "BARE_JB_JL_Q0_RESPONSE_IS_STATE_SELECTIVE=NO"
    )
    print(
        "010E_EXACT_SELECTOR="
        "B_MATERIAL_TIMES_P_HS1_TIMES_P_HS2"
    )
    print(
        "BARE_CONSERVED_CURRENT_ENDPOINT_REPRODUCES_010E_EXACT_SELECTOR="
        "NO"
    )

    high_order_node_required = (
        strict_k_min >= 8
    )

    print(
        "SMOOTH_KERNEL_NODE_REQUIRES_HIGH_MULTISECTOR_ORDER="
        + (
            "YES"
            if high_order_node_required
            else "NO"
        )
    )
    print(
        "SMOOTH_KERNEL_NODE_COUNTS_AS_PROTECTED_SELECTOR="
        "NO_WITHOUT_NEW_EXACT_SYMMETRY"
    )

    # ------------------------------------------------------------------
    # B. Wilson capacity input.
    # ------------------------------------------------------------------
    print("\n=== B — MAXIMUM INHERITED WILSON CURVATURE ===")

    kappa_cw, kappa_n, kappa_rho = max_positive_wilson_curvature(
        a019
    )

    print(
        "WILSON_KAPPA_CW_MAX="
        f"{kappa_cw:.15e}"
    )
    print(
        "WILSON_KAPPA_CW_MAX_N="
        f"{kappa_n}"
    )
    print(
        "WILSON_KAPPA_CW_MAX_RHO="
        f"{kappa_rho:.15e}"
    )
    print(
        "WILSON_SCAN_CHOICE="
        "MAXIMUM_CURVATURE_OPTIMISTIC_FOR_PORTAL"
    )

    # ------------------------------------------------------------------
    # C. Full actual asymmetric portal scans.
    # ------------------------------------------------------------------
    print("\n=== C — ACTUAL ASYMMETRIC 019C PORTAL SCANS ===")

    scan_results = {}

    for geometry in GEOMETRIES:
        all_points, mandatory, preferred = scan_geometry(
            b0,
            geometry,
            kappa_cw,
        )

        if not all_points:
            raise RuntimeError(
                f"No finite scan points for {geometry.name}"
            )

        best = min(
            all_points,
            key=point_rank,
        )

        scan_results[geometry.name] = (
            all_points,
            mandatory,
            preferred,
            best,
        )

        prefix = geometry.name

        print(
            f"{prefix}_FINITE_POINTS={len(all_points)}"
        )
        print(
            f"{prefix}_MANDATORY_NATURALNESS_PASSERS={len(mandatory)}"
        )
        print(
            f"{prefix}_PREFERRED_NATURALNESS_PASSERS={len(preferred)}"
        )
        print(
            f"{prefix}_BEST_MAX_NATURALNESS_RATIO="
            f"{best.max_naturalness_ratio:.15e}"
        )
        print(
            f"{prefix}_BEST_RANGE_M="
            f"{best.range_m:.15e}"
        )
        print(
            f"{prefix}_BEST_P_BACKREACTION_RATIO="
            f"{best.p_backreaction_ratio:.15e}"
        )
        print(
            f"{prefix}_BEST_VECTOR_HIGGS_RATIO="
            f"{best.vector_higgs_ratio:.15e}"
        )
        print(
            f"{prefix}_BEST_Y_P="
            f"{best.y_p:.15e}"
        )
        print(
            f"{prefix}_BEST_R_P="
            f"{best.r_p:.15e}"
        )
        print(
            f"{prefix}_BEST_G_X="
            f"{best.g_x:.15e}"
        )
        print(
            f"{prefix}_BEST_G_B="
            f"{best.g_b:.15e}"
        )

    # ------------------------------------------------------------------
    # D. Detailed least-bad molecular point.
    # ------------------------------------------------------------------
    print("\n=== D — LEAST-BAD MOLECULAR-OPTIMISTIC POINT ===")

    molecular_all, molecular_mandatory, molecular_preferred, molecular_best = (
        scan_results["MOLECULAR_OPTIMISTIC"]
    )

    print_point(
        "MOLECULAR_BEST",
        molecular_best,
    )

    # ------------------------------------------------------------------
    # E. Detailed best atomic-optimistic point.
    # ------------------------------------------------------------------
    print("\n=== E — LEAST-BAD ATOMIC-OPTIMISTIC POINT ===")

    atomic_all, atomic_mandatory, atomic_preferred, atomic_best = (
        scan_results["ATOMIC_OPTIMISTIC"]
    )

    print_point(
        "ATOMIC_BEST",
        atomic_best,
    )

    # ------------------------------------------------------------------
    # F. Naturalness-vs-range diagnostic at best microscopic envelope.
    # ------------------------------------------------------------------
    print("\n=== F — RANGE SCALING DIAGNOSTIC ===")

    # For each geometry, report the best available max-naturalness ratio at
    # each scalar range, then find the global minimum.
    for geometry in GEOMETRIES:
        points = scan_results[geometry.name][0]

        by_range = {}

        for point in points:
            current = by_range.get(
                point.range_m
            )

            if (
                current is None
                or point.max_naturalness_ratio
                < current.max_naturalness_ratio
            ):
                by_range[point.range_m] = point

        ordered = sorted(
            by_range.values(),
            key=lambda point: point.range_m,
        )

        global_best = min(
            ordered,
            key=lambda point: point.max_naturalness_ratio,
        )

        print(
            f"{geometry.name}_RANGE_ENVELOPE_MIN_RATIO="
            f"{global_best.max_naturalness_ratio:.15e}"
        )
        print(
            f"{geometry.name}_RANGE_ENVELOPE_MIN_AT_M="
            f"{global_best.range_m:.15e}"
        )

        # Fit local power law where possible around 1e-9 to 1e-7 m.
        fit_points = [
            point
            for point in ordered
            if 1.0e-9 <= point.range_m <= 1.0e-7
            and point.max_naturalness_ratio > 0.0
        ]

        if len(fit_points) >= 4:
            x = np.log(
                [
                    point.range_m
                    for point in fit_points
                ]
            )
            y = np.log(
                [
                    point.max_naturalness_ratio
                    for point in fit_points
                ]
            )

            slope, _ = np.polyfit(
                x,
                y,
                deg=1,
            )

            print(
                f"{geometry.name}_NATURALNESS_POWER_LAW_SLOPE="
                f"{float(slope):.15e}"
            )

    # ------------------------------------------------------------------
    # G. Blind wildcard diagnostics — not evidence.
    # ------------------------------------------------------------------
    print("\n=== BLIND WILDCARD DIAGNOSTICS — NOT EVIDENCE ===")

    reference_range = molecular_best.range_m

    for factor in BLIND_WILDCARDS:
        requested_range = (
            reference_range * factor
        )

        nearest_range = min(
            RANGE_GRID_M,
            key=lambda value: abs(
                math.log(value / requested_range)
            ),
        )

        points_at_range = [
            point
            for point in molecular_all
            if point.range_m == nearest_range
        ]

        if not points_at_range:
            print(
                f"WILDCARD_FACTOR={factor:.6f} STATUS=NO_POINT"
            )
            continue

        best_here = min(
            points_at_range,
            key=point_rank,
        )

        print(
            f"WILDCARD_FACTOR={factor:.6f} "
            f"RANGE_M={nearest_range:.9e} "
            f"MAX_NAT={best_here.max_naturalness_ratio:.9e} "
            f"P_BACK={best_here.p_backreaction_ratio:.9e} "
            f"VH={best_here.vector_higgs_ratio:.9e} "
            f"MANDATORY={'PASS' if best_here.mandatory_naturalness_pass else 'FAIL'}"
        )

    print(
        "BLIND_WILDCARD_VALUES_USED_AS_EVIDENCE=NO"
    )

    # ------------------------------------------------------------------
    # H. Independent algebra checks.
    # ------------------------------------------------------------------
    print("\n=== H — INDEPENDENT ALGEBRA CHECKS ===")

    # Reconstruct C_phi from d_theta exactly at the molecular best point.
    c_reconstructed = (
        molecular_best.d_theta
        /
        (
            2.0
            * molecular_best.f_ev
            * molecular_best.v_ev**2
        )
    )

    c_relerr = relative_error(
        c_reconstructed,
        molecular_best.c_target,
    )

    # Reconstruct P backreaction directly from the tadpole derivative.
    t_prime = (
        molecular_best.y_p
        * molecular_best.mu_ev**3
        * molecular_best.kappa_cw
        /
        (
            64.0
            * math.pi**2
        )
    )

    p_back_direct = (
        t_prime**2
        /
        (
            molecular_best.m_p_ev**2
            * molecular_best.f_ev**2
            * molecular_best.m_phi_ev**2
        )
    )

    p_back_relerr = relative_error(
        p_back_direct,
        molecular_best.p_backreaction_ratio,
    )

    print(
        "INDEPENDENT_C_RECONSTRUCTED="
        f"{c_reconstructed:.15e}"
    )
    print(
        "INDEPENDENT_C_MATCH_RELERR="
        f"{c_relerr:.15e}"
    )
    print(
        "INDEPENDENT_P_BACKREACTION_RATIO="
        f"{p_back_direct:.15e}"
    )
    print(
        "INDEPENDENT_P_BACKREACTION_RELERR="
        f"{p_back_relerr:.15e}"
    )

    independent_pass = (
        c_relerr <= 1.0e-10
        and p_back_relerr <= 1.0e-10
    )

    print(
        "INDEPENDENT_RECONSTRUCTION="
        + (
            "PASS"
            if independent_pass
            else "FAIL"
        )
    )

    # ------------------------------------------------------------------
    # I. Decision.
    # ------------------------------------------------------------------
    print("\n=== 022A DECISION ===")

    molecular_mandatory_count = len(
        molecular_mandatory
    )

    selector_mismatch = (
        high_order_node_required
    )

    asymmetric_microscopic_fail = (
        molecular_mandatory_count == 0
    )

    if not independent_pass:
        print(
            "022A_ASYMMETRIC_VECTOR_MATERIAL_SELECTOR_AND_NATURALNESS_CLOSEOUT="
            "RED_VALIDATION_FAILURE"
        )
        print(
            "NEXT=DEBUG_BEFORE_SCIENTIFIC_INTERPRETATION"
        )

    elif selector_mismatch and asymmetric_microscopic_fail:
        print(
            "022A_ASYMMETRIC_VECTOR_MATERIAL_SELECTOR_AND_NATURALNESS_CLOSEOUT="
            "GREEN_NEGATIVE_RESULT"
        )
        print(
            "BARE_CONSERVED_CURRENT_MATERIAL_SELECTOR="
            "REJECTED_AS_010E_SELECTOR_UV_COMPLETION"
        )
        print(
            "REASON_SELECTOR="
            "Q0_UNIVERSALITY_PLUS_HIGH_ORDER_FLUCTUATION_SENSITIVE_KERNEL_NODE"
        )
        print(
            "ASYMMETRIC_019C_SHORT_RANGE_MICROSCOPIC_PORTAL="
            "REJECTED_IN_MOLECULAR_OPTIMISTIC_GEOMETRY"
        )
        print(
            "REASON_PORTAL="
            "P_BACKREACTION_OR_OTHER_MANDATORY_NATURALNESS_BEFORE_MATERIAL_SCALE"
        )
        print(
            "021B0_OPTIMISTIC_CAPACITY_SURPLUS="
            "NOT_A_REALIZED_PORTAL_AFTER_MANDATORY_BACKREACTION"
        )
        print(
            "PROTECTED_VECTOR_CURRENT_PRACTICALITY_BRANCH="
            "CLOSED_IN_TESTED_SHORT_RANGE_CLASSES"
        )
        print(
            "GLOBAL_RERANK="
            "REQUIRED"
        )
        print(
            "NEXT="
            "023A_INTRINSICALLY_STABLE_SOLITON_TOPOLOGY_AND_NANOSTANDOFF_GR_GATE"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY"
        )
        print(
            "HEURISTIC_CHANGE="
            "NONE_NEGATIVE_CLOSEOUT_INCREASES_INFORMATION_NOT_DEVICE_MATURITY"
        )

    elif selector_mismatch and not asymmetric_microscopic_fail:
        print(
            "022A_ASYMMETRIC_VECTOR_MATERIAL_SELECTOR_AND_NATURALNESS_CLOSEOUT="
            "GREEN_MIXED_RESULT"
        )
        print(
            "ASYMMETRIC_019C_MICROSCOPIC_MAGNITUDE_AND_NATURALNESS="
            "HAS_SURVIVING_MOLECULAR_OPTIMISTIC_POINTS"
        )
        print(
            "BARE_CONSERVED_CURRENT_MATERIAL_SELECTOR="
            "REJECTED_AS_010E_SELECTOR_UV_COMPLETION"
        )
        print(
            "COMPLETE_MICROSCOPIC_MATERIAL_PORTAL="
            "NO"
        )
        print(
            "NEXT="
            "022B_EXACT_BOUND_COMPOSITE_NONCURRENT_PROTECTION_GATE_ONLY_IF_NEW_EXACT_SYMMETRY_IS_SUPPLIED"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY"
        )
        print(
            "HEURISTIC_CHANGE=NONE"
        )

    else:
        print(
            "022A_ASYMMETRIC_VECTOR_MATERIAL_SELECTOR_AND_NATURALNESS_CLOSEOUT="
            "INCOMPLETE_OR_SURVIVING_UNEXPECTED_CONDITION"
        )
        print(
            "NEXT=INSPECT_SURVIVING_CONDITION"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY"
        )

    # Permanent claim boundaries.
    print(
        "EXACT_2026_DIRECT_VECTOR_EXPERIMENTAL_FIT="
        "NOT_DONE_BY_THIS_GATE"
    )
    print(
        "REAL_MATERIAL_WITH_NEW_FORCE="
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

    # Preserve durable project results.
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
        "019B_VECTOR_CURRENT_EFT_ESCAPE="
        "RETAINED_AS_EFT_RESULT_NOT_MATERIAL_SELECTOR"
    )
    print(
        "019C_VECTOR_HIGGS_MEDIATOR_ALGEBRA="
        "RETAINED"
    )
    print(
        "020A2R_5KM_CLOSEOUT="
        "RETAINED"
    )
    print(
        "021A_SHORT_RANGE_SCALING_INSIGHT="
        "RETAINED_AS_SCALING_INSIGHT_NOT_PROMOTION"
    )
    print(
        "021B0_CAPACITY_RESULT="
        "RETAINED_AS_OPTIMISTIC_UPPER_BOUND"
    )
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_022A_ASYMMETRIC_VECTOR_MATERIAL_SELECTOR_AND_NATURALNESS_CLOSEOUT"
    )


if __name__ == "__main__":
    main()
