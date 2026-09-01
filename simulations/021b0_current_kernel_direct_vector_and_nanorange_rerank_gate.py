#!/usr/bin/env python3
"""021B0 — current-kernel, direct-vector, and nanorange rerank gate.

PURPOSE
-------
Audit the 021A short-range isotope-sign Wilson/vector proposal before any
promotion of the project heuristic, then perform the cheapest decisive
nanorange rerank if the 021A 100-micrometer-to-10-centimeter implementation
fails.

021A reported a large robust microscopic basin under three key assumptions:

1. the scalar charge of isotope-enriched material could be inferred from the
   integrated conserved charge

       Q_X = L - c B;

2. the keV-scale heavy vectors that generate the Wilson-dependent
   current-current kernel could couple to ordinary baryon/lepton currents with
   order-unity gauge couplings without first producing unacceptable ordinary
   atomic or nuclear effects;

3. if the old 100-micrometer lower-range boundary fails, shorter-range
   lamellar geometries might improve the microscopic scaling.

This run checks all three in fail-closed order.

ACTIVE SCIENTIFIC QUESTION
--------------------------
Does the specific 021A short-range portal survive when:

A. the complete dinuclear Fe(II) host formula unit is used rather than an
   isolated Fe atom;

B. the finite heavy-vector propagator is used inside the composite material
   rather than replacing the current-current response by a total-charge
   product;

C. the direct U(1)_X electron coupling and direct U(1)_B nuclear self-energy
   are included before the Wilson scalar response is considered;

D. asymmetric baryon/electron vector couplings are allowed and the portal is
   given an intentionally optimistic analytic upper bound;

E. the source/payload geometry is extended into a nanolamellar regime only if
   the old 021A range is closed.

The gate is intentionally designed to FALSIFY the 021A promotion if any
mandatory ordinary-matter effect is already fatal.

UPSTREAM CLAIM BOUNDARY
-----------------------
The following prior results remain valid regardless of this run:

    006D constructive finite positive-energy linearized-GR result
    018B microscopic field-existence result
    018C m=2 stability falsification of the specific KLS wall-rim architecture
    019A protected Wilson-line witness
    019B anomaly-free B/L vector-current endpoint
    019C renormalizable heavy-vector/Higgs mediator algebra
    020A1/020A2 isospectral vector-response mathematics
    020A2R closeout of the tested 5-km minimal classes

021B0 audits only the new 021A short-range/isotope implementation and a
strictly optimistic nanorange capacity escape.

REAL DINUCLEAR HOST BOOKKEEPING
-------------------------------
The low-temperature dinuclear Fe(II) host used in the project literature has
the formula

    Fe2 C40 H30 N16 S4

for

    [{Fe(phdia)(NCS)2}2(phdia)]

with phdia = 4,7-phenanthroline-5,6-diamine.

Using the dominant light-isotope mass numbers for the non-Fe atoms,

    12C, 1H, 14N, 32S,

the neutral formula contains

    L_tot = 498 electrons.

If both Fe sites are 54Fe,

    B_54 = 970.

If both Fe sites are 58Fe,

    B_58 = 978.

The coefficient that makes the INTEGRATED formula-unit charges exactly
opposite is therefore

    c_formula
      =
    2 L_tot / (B_54 + B_58)
      =
    249/487.

The corresponding integrated charge magnitude is

    |Q_X|/L_tot
      =
    (B_58-B_54)/(B_54+B_58)
      =
    2/487,

so the coefficient-normalization penalty is

    487/2 = 243.5,

not the isolated-Fe factor 28 used by 021A.

FINITE-MEDIATOR COMPOSITE KERNEL
--------------------------------
The 019C Higgs/vector bridge does not literally create a pointwise
C_phi phi J_B J_X interaction at arbitrarily high momentum.  For equal heavy
vector masses M_V, differentiating the off-diagonal propagator gives the
finite-range kernel

    K(r)
      proportional to
    exp(-M_V r)

(up to an overall positive normalization irrelevant to the sign test).

Therefore a composite scalar response must be matched at the pair-kernel
level, schematically

    Q_phi
      proportional to
    sum_(B,L) K(r_BL)
      -
    c sum_(B,B, i != j) K(r_BB).

The B-B term is an ORDERED-pair sum because it arises from J_B J_B.
Self-contractions are excluded from the conservative bound.

For an Fe nucleus all distinct baryon pairs lie within a diameter

    2 R_A,
    R_A = 1.2 A^(1/3) fm.

Hence

    K_BB >= exp(-2 R_A/lambda_V).

Every B-L kernel satisfies

    K_BL <= 1.

This gives a rigorous survival-favoring upper bound

    Q_phi^upper(A)
      =
    A Z
      -
    c A(A-1) exp(-2 R_A/lambda_V).

If even this upper bound is negative, no possible electron wavefunction can
make that Fe site positively charged under the tested finite-range kernel.

This does not yet calculate the full molecular kernel.  Its purpose is to
determine whether the integrated-charge sign premise of 021A is even
compatible with the underlying finite-range current operator.

DIRECT U(1)_X ELECTRON PREFLIGHT
--------------------------------
An electron has

    B = 0
    X = L - c B = 1.

Therefore the U(1)_X vector couples directly to electrons with strength g_X.

For a vector of mass M_X, the ordinary one-loop contribution to the electron
anomalous magnetic moment is

    Delta a_e
      =
    g_X^2/(8 pi^2)
    integral_0^1
    [2 z (1-z)^2]
    /
    [(1-z)^2 + (M_X/m_e)^2 z]
    dz.

021B0 does NOT claim an exact 2026 experimental fit.  Instead it adopts an
intentionally loose preflight allowance

    |Delta a_e| <= 1e-6.

This is many orders less demanding than a precision-electron analysis and is
used only as a cheap rejection gate.  If the portal cannot survive even this
loose allowance, an exact experimental refit cannot rescue it.

DIRECT U(1)_B NUCLEAR SELF-ENERGY PREFLIGHT
-------------------------------------------
For a vector whose Compton wavelength is long compared with an Fe nucleus,
the repulsive baryon-vector self-energy of a uniform nuclear sphere is

    U_B
      approximately
    (3/5) alpha_B A(A-1) hbar c / R_A,

where

    alpha_B = g_B^2/(4 pi).

To bias the test heavily in favor of survival, require only

    U_B <= 100 percent

of a rough Fe nuclear binding-energy scale

    E_bind = 8 MeV * A.

This is not a precision nuclear-structure constraint.  It is an absurdly
permissive ordinary-matter consistency ceiling.

For mediator masses approaching the inverse nuclear radius, the code includes
a finite-range suppression factor rather than using the long-range Coulomb
limit blindly.

ASYMMETRIC-COUPLING PORTAL UPPER BOUND
--------------------------------------
The 019C bridge can use unequal g_B and g_X.

For

    S_+ : (1,+1)
    S_- : (1,-1),

the small-d current-current response itself is independent of g_B g_X after
the heavy vectors are integrated out, but both vector masses must still lie
above the material-EFT floor:

    M_B = sqrt(2) g_B v
    M_X = sqrt(2) g_X v.

Thus the smaller gauge coupling forces a larger bridge VEV:

    v >= M_min/[sqrt(2) min(g_B,g_X)].

The run derives an OPTIMISTIC analytic capacity bound by simultaneously
granting the portal:

    f <= reduced Planck scale;
    y_P at the perturbative boundary;
    messenger scale chosen to maximize response subject to the Wilson mass;
    heavy vectors, P, and radial Higgs exactly at the minimum allowed mass;
    quartic lambda_S at the minimum consistent with the radial mass;
    bridge Hessian exactly at the declared stability floor;
    the maximum positive Wilson curvature found in the 019A scan;
    no penalty from P backreaction;
    no vector/Higgs CW naturalness penalty;
    no stellar/cosmological penalty;
    no exact fifth-force constraint.

With Hessian minimum eigenvalue fraction h, the resulting upper envelope is

    C_max
      =
    (1-h)
    g_min^3
    m_phi^(3/2)
    kappa_CW^(1/4)
    sqrt(f_max)
    /
    M_min^5,

when y_P is saturated at sqrt(4 pi).

This is an UPPER BOUND, not a realized model point.

If even this bound lies below the required C_target, the tested direct-vector
implementation is closed.

NANOLAMELLAR CAPACITY ORACLE
----------------------------
If the 021A range is closed, search

    0.25 nm <= lambda_phi <= 100 micrometers.

For the oracle use a repeating planar cell:

    payload layer thickness = lambda_phi
    source layer thickness  = 5 lambda_phi
    gap/spacer               = 0.1 lambda_phi
    total pitch              = 16 lambda_phi.

For a 1-kg payload spread over 1 m^2,

    N_layers
      =
    M_payload/(rho A lambda_phi),

and

    stack_height
      =
    N_layers * 16 lambda_phi
      =
    16 M_payload/(rho A),

so the stack height is independent of mediator range.

This is a capacity result only.  A nanorange crossing does NOT establish:

    a real nanolamellar SCO material;
    a valid opposite-sign material kernel;
    experimental safety;
    manufacturability;
    thermal/control closure;
    practical antigravity.

TARGET NORMALIZATIONS
---------------------
Three target normalizations are reported:

1. 021A isolated-Fe assumption:
       penalty = 28

2. actual dinuclear formula-unit integrated-charge normalization:
       penalty = 487/2 = 243.5

3. an intentionally optimistic "multi-isotope oracle" normalization:
       penalty = 205/11 approximately 18.636

The third is NOT an established material.  It exists only to ask whether even
an unrealistically favorable isotope normalization leaves any structural
nanorange capacity.

PROMOTION / STOP RULES
----------------------
This gate CANNOT itself promote the heuristic to 70 or 80 percent.

Possible outcomes:

A. If the 021A kernel sign fails and direct-vector constraints close the full
   100-micrometer-to-10-centimeter range, record 021A as not promotable.

B. If no nanorange oracle crossing exists above 0.25 nm, close this entire
   direct-vector short-range branch and globally rerank.

C. If an oracle crossing exists, preserve ONLY:

       NANOLAMELLAR_SCALING_ESCAPE =
       SUPPORTED_AS_CAPACITY_PREFLIGHT

   and proceed to a new 022A kernel-level current/operator construction.

A later 70-72 percent promotion requires an actual microscopic nanolamellar
portal with a physically valid material charge sign and experimental safety.

A later 80-85 percent milestone additionally requires complete operator,
experimental, stellar/cosmological, real-material, finite-payload, and
full-control-cycle closure.

UNITS
-----
Natural units hbar=c=1 are used where stated.
SI is used for finite-source force geometry.
Mass/energy inputs are in eV unless explicitly labeled MeV.
Lengths are explicitly labeled meters or femtometers.

VALIDATION
----------
The run performs:

- exact upstream 021A source hash and GREEN marker audit;
- exact rational formula-unit charge reconstruction;
- independent rational check of c_formula;
- finite-vector kernel sign upper bound at the 021A selected point;
- exact numerical electron-g-2 integration;
- small-M analytic electron-g-2 cross-check;
- analytic nuclear self-energy ceiling plus finite-range correction;
- asymmetric-coupling optimistic portal upper bound;
- full 021A-range deficit scan;
- nanorange capacity scan;
- independent power-law fit of deficit versus scalar range;
- lamellar 1-kg layer-count/height reconstruction;
- blind wildcard checks, explicitly not evidence.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_021B0_CURRENT_KERNEL_DIRECT_VECTOR_AND_NANORANGE_RERANK_GATE
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

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parents[1]

A_SOURCE = ROOT / "simulations/019a_wilson_line_sequestered_pair_scalar_uv_protection_gate.py"
B_SOURCE = ROOT / "simulations/019b_anomaly_free_sm_material_endpoint_and_one_body_mixing_gate.py"
C_SOURCE = ROOT / "simulations/019c_vector_wilson_portal_minimal_uv_construction_gate.py"
A21_SOURCE = ROOT / "simulations/021a_short_range_isotope_sign_wilson_vector_portal_promotion_gate.py"

A_LOG = ROOT / "results/logs/019a_wilson_line_sequestered_pair_scalar_uv_protection_gate.log"
B_LOG = ROOT / "results/logs/019b_anomaly_free_sm_material_endpoint_and_one_body_mixing_gate.log"
C_LOG = ROOT / "results/logs/019c_vector_wilson_portal_minimal_uv_construction_gate.log"
R_LOG = ROOT / "results/logs/020a2r_exact_bl_running_and_hp_global_naturalness_closeout.log"
A21_LOG = ROOT / "results/logs/021a_short_range_isotope_sign_wilson_vector_portal_promotion_gate.log"

EXPECTED_021A_SHA256 = "aedf8be83f17efc6e7e07f8f25630744a41b8ac7aa76909bc5f183f47565e372"

# ---------------------------------------------------------------------------
# Inherited project constants.
# ---------------------------------------------------------------------------

C_REF = 9.536416387852626e-20
ALPHA_ACTIVATED_REF = 1.558991777087370e5
MATERIAL_EFT_CUTOFF_EV = 657.7566
PREFERRED_MASS_MARGIN = 2.0

G_SI = 6.67430e-11
G_ACCEL = 9.80665
SOURCE_DENSITY_KG_M3 = 3000.0
PAYLOAD_DENSITY_KG_M3 = 3000.0
PAYLOAD_MASS_KG = 1.0

HBARC_EV_M = 1.973269804e-7
HBARC_MEV_FM = 197.3269804
M_E_EV = 510_998.95069
MPL_REDUCED_EV = 2.435e27

# ---------------------------------------------------------------------------
# Real dinuclear host formula Fe2 C40 H30 N16 S4.
# ---------------------------------------------------------------------------

FORMULA_COUNTS = {
    "Fe": 2,
    "C": 40,
    "H": 30,
    "N": 16,
    "S": 4,
}

ATOMIC_Z = {
    "Fe": 26,
    "C": 6,
    "H": 1,
    "N": 7,
    "S": 16,
}

LIGHT_A = {
    "C": 12,
    "H": 1,
    "N": 14,
    "S": 32,
}

FE54_A = 54
FE58_A = 58

# ---------------------------------------------------------------------------
# Preflight constraints.
# ---------------------------------------------------------------------------

# Deliberately loose: this is a cheap rejection test, not the exact 2026 fit.
DELTA_AE_PREFLIGHT_MAX = 1.0e-6

# Deliberately loose nuclear criterion: permit vector self-energy equal to the
# entire rough Fe binding energy.
NUCLEAR_BINDING_MEV_PER_NUCLEON = 8.0
NUCLEAR_SELF_ENERGY_FRACTION_MAX = 1.0

NUCLEAR_RADIUS_R0_FM = 1.2

# Bridge stability threshold inherited from 021A.
HESSIAN_MIN_FRACTION = 0.25

# Perturbative boundary for y_P.
Y_P_MAX = math.sqrt(4.0 * math.pi)

# ---------------------------------------------------------------------------
# Oracle target normalizations.
# ---------------------------------------------------------------------------

PENALTY_021A_ISOLATED_FE = 28.0
PENALTY_FORMULA_UNIT = 487.0 / 2.0

# Intentionally optimistic oracle only; not a demonstrated material.
PENALTY_MULTI_ISOTOPE_ORACLE = 205.0 / 11.0

# ---------------------------------------------------------------------------
# Range scans.
# ---------------------------------------------------------------------------

OLD_RANGE_MIN_M = 1.0e-4
OLD_RANGE_MAX_M = 1.0e-1

NANO_RANGE_MIN_M = 2.5e-10
NANO_RANGE_MAX_M = OLD_RANGE_MIN_M

OLD_RANGE_GRID = np.geomspace(OLD_RANGE_MIN_M, OLD_RANGE_MAX_M, 80)
NANO_RANGE_GRID = np.geomspace(NANO_RANGE_MIN_M, NANO_RANGE_MAX_M, 220)

# Heavy-vector floor.  The optimistic capacity bound always prefers the
# smallest allowed vector mass, so scanning upward can only hurt unless direct
# constraints themselves require it.
M_VECTOR_MIN_EV = PREFERRED_MASS_MARGIN * MATERIAL_EFT_CUTOFF_EV

# For the direct-vector audit we also show masses through 100 MeV.
M_VECTOR_AUDIT_GRID_EV = np.geomspace(
    M_VECTOR_MIN_EV,
    1.0e8,
    120,
)

# ---------------------------------------------------------------------------
# Lamellar geometry.
# ---------------------------------------------------------------------------

LAYER_AREA_M2 = 1.0
PAYLOAD_LAYER_THICKNESS_IN_LAMBDA = 1.0
SOURCE_LAYER_THICKNESS_IN_LAMBDA = 5.0
GAP_IN_LAMBDA = 0.1
CELL_PITCH_IN_LAMBDA = 16.0

RADIAL_EDGE_MARGIN_LAMBDA = 10.0

# ---------------------------------------------------------------------------
# Blind wildcard diagnostics only.
# ---------------------------------------------------------------------------

BLIND_WILDCARDS = (1.6, 1.875, 3.125, 0.625, 5.0)


@dataclass(frozen=True)
class FormulaUnit:
    """Exact neutral formula-unit bookkeeping."""

    electrons: int
    baryons_54: int
    baryons_58: int
    c_formula: Fraction
    relative_charge: Fraction
    penalty: Fraction


@dataclass(frozen=True)
class DirectVectorBounds:
    """Ordinary-matter direct-vector coupling ceilings."""

    vector_mass_ev: float
    g_x_ae_max: float
    g_b_nuclear_max: float
    g_min_max: float
    delta_ae_at_g_021a: float
    nuclear_fraction_at_g_021a: float


@dataclass(frozen=True)
class CapacityPoint:
    """One optimistic scalar-range capacity point."""

    range_m: float
    m_phi_ev: float
    alpha_required: float
    c_target_021a: float
    c_target_formula: float
    c_target_oracle: float
    c_max: float
    deficit_021a: float
    deficit_formula: float
    deficit_oracle: float
    layer_count: float
    stack_height_m: float


def require_marker(path: Path, marker: str) -> None:
    """Require one exact upstream scientific marker."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream log: {path}")

    text = path.read_text(errors="replace")
    if marker not in text:
        raise RuntimeError(
            f"Missing required marker in {path.name}: {marker}"
        )


def exact_scalar(path: Path, prefix: str) -> float:
    """Read one exact scalar prefix from an executed log."""

    if not path.exists():
        raise RuntimeError(f"Missing log: {path}")

    pattern = re.compile(
        rf"^{re.escape(prefix)}([+\-0-9.eE]+)$",
        re.MULTILINE,
    )

    match = pattern.search(
        path.read_text(errors="replace")
    )

    if match is None:
        raise RuntimeError(
            f"Could not find {prefix!r} in {path.name}"
        )

    value = float(match.group(1))

    if not math.isfinite(value):
        raise RuntimeError(
            f"Nonfinite value for {prefix!r}"
        )

    return value


def sha256(path: Path) -> str:
    """Return SHA-256 for one source file."""

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
    """Return a stable relative error."""

    return abs(a - b) / max(
        abs(a),
        abs(b),
        1.0e-300,
    )


def formula_unit() -> FormulaUnit:
    """Reconstruct the real dinuclear host formula-unit charge exactly."""

    electrons = sum(
        FORMULA_COUNTS[element] * ATOMIC_Z[element]
        for element in FORMULA_COUNTS
    )

    non_fe_baryons = sum(
        FORMULA_COUNTS[element] * LIGHT_A[element]
        for element in LIGHT_A
    )

    baryons_54 = (
        non_fe_baryons
        + FORMULA_COUNTS["Fe"] * FE54_A
    )

    baryons_58 = (
        non_fe_baryons
        + FORMULA_COUNTS["Fe"] * FE58_A
    )

    c_formula = Fraction(
        2 * electrons,
        baryons_54 + baryons_58,
    )

    relative_charge = Fraction(
        baryons_58 - baryons_54,
        baryons_54 + baryons_58,
    )

    penalty = Fraction(
        relative_charge.denominator,
        relative_charge.numerator,
    )

    return FormulaUnit(
        electrons=electrons,
        baryons_54=baryons_54,
        baryons_58=baryons_58,
        c_formula=c_formula,
        relative_charge=relative_charge,
        penalty=penalty,
    )


def nuclear_radius_fm(A: int) -> float:
    """Return R_A = r0 A^(1/3) in fm."""

    return NUCLEAR_RADIUS_R0_FM * A ** (1.0 / 3.0)


def vector_range_fm(vector_mass_ev: float) -> float:
    """Return heavy-vector Compton wavelength in fm."""

    vector_mass_mev = vector_mass_ev * 1.0e-6

    return HBARC_MEV_FM / vector_mass_mev


def fe_site_kernel_upper_bound(
    A: int,
    c_value: float,
    vector_mass_ev: float,
) -> tuple[float, float, float]:
    """Return a rigorous survival-favoring Fe-site kernel upper bound.

    Every B-L pair is granted K=1.

    Every distinct B-B pair is assigned only the minimum kernel value allowed
    by the nuclear diameter:

        K_BB >= exp(-2 R_A/lambda_V).

    Thus if the returned Q_upper is negative, the actual Fe-site kernel charge
    must also be negative.
    """

    Z = 26

    radius = nuclear_radius_fm(A)
    lambda_v = vector_range_fm(vector_mass_ev)

    k_bb_min = math.exp(
        -2.0 * radius / lambda_v
    )

    bl_upper = float(A * Z)

    bb_lower = (
        float(A * (A - 1))
        * k_bb_min
    )

    q_upper = (
        bl_upper
        - c_value * bb_lower
    )

    return q_upper, bl_upper, bb_lower


def electron_gminus2_integral(vector_mass_ev: float) -> float:
    """Return the dimensionless vector g-2 integral I(M/m_e)."""

    ratio = vector_mass_ev / M_E_EV

    def integrand(z: float) -> float:
        numerator = (
            2.0
            * z
            * (1.0 - z) ** 2
        )

        denominator = (
            (1.0 - z) ** 2
            + ratio**2 * z
        )

        return numerator / denominator

    value, error = quad(
        integrand,
        0.0,
        1.0,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
        limit=400,
    )

    if not math.isfinite(value):
        raise RuntimeError(
            "Nonfinite electron g-2 integral"
        )

    return value


def delta_ae_vector(
    g_x: float,
    vector_mass_ev: float,
) -> float:
    """Return ordinary one-loop vector contribution to electron a_e."""

    integral = electron_gminus2_integral(
        vector_mass_ev
    )

    return (
        g_x**2
        / (8.0 * math.pi**2)
        * integral
    )


def g_x_max_from_ae(vector_mass_ev: float) -> float:
    """Solve the deliberately loose electron-g-2 preflight ceiling."""

    integral = electron_gminus2_integral(
        vector_mass_ev
    )

    return math.sqrt(
        DELTA_AE_PREFLIGHT_MAX
        * 8.0
        * math.pi**2
        / integral
    )


def nuclear_yukawa_suppression(
    vector_mass_ev: float,
    A: int,
) -> float:
    """Return a conservative finite-range suppression for nuclear self-energy.

    The exact self-energy of a Yukawa-interacting uniform sphere has a known
    closed form.  For this preflight, use a deliberately conservative lower
    estimate of the interaction fraction

        exp(-2 R/lambda_V),

    which understates the vector self-energy and therefore weakens the
    nuclear constraint.
    """

    radius = nuclear_radius_fm(A)
    lambda_v = vector_range_fm(vector_mass_ev)

    return math.exp(
        -2.0 * radius / lambda_v
    )


def nuclear_vector_self_energy_mev(
    g_b: float,
    vector_mass_ev: float,
    A: int = 56,
) -> float:
    """Return a conservative Fe nuclear baryon-vector self-energy estimate."""

    alpha_b = g_b**2 / (
        4.0 * math.pi
    )

    radius = nuclear_radius_fm(A)

    unsuppressed = (
        3.0
        / 5.0
        * alpha_b
        * A
        * (A - 1)
        * HBARC_MEV_FM
        / radius
    )

    return (
        unsuppressed
        * nuclear_yukawa_suppression(
            vector_mass_ev,
            A,
        )
    )


def g_b_max_from_nuclear(
    vector_mass_ev: float,
    A: int = 56,
) -> float:
    """Return the deliberately permissive baryon-vector coupling ceiling."""

    binding = (
        NUCLEAR_BINDING_MEV_PER_NUCLEON
        * A
        * NUCLEAR_SELF_ENERGY_FRACTION_MAX
    )

    unit_energy = nuclear_vector_self_energy_mev(
        1.0,
        vector_mass_ev,
        A,
    )

    if unit_energy <= 0.0:
        raise RuntimeError(
            "Invalid nuclear unit self-energy"
        )

    return math.sqrt(
        binding / unit_energy
    )


def direct_vector_bounds(
    vector_mass_ev: float,
    g_021a: float,
) -> DirectVectorBounds:
    """Return both direct-vector ceilings at one mediator mass."""

    gx_max = g_x_max_from_ae(
        vector_mass_ev
    )

    gb_max = g_b_max_from_nuclear(
        vector_mass_ev
    )

    delta_ae = delta_ae_vector(
        g_021a,
        vector_mass_ev,
    )

    binding = (
        NUCLEAR_BINDING_MEV_PER_NUCLEON
        * 56
    )

    nuclear_fraction = (
        nuclear_vector_self_energy_mev(
            g_021a,
            vector_mass_ev,
            56,
        )
        / binding
    )

    return DirectVectorBounds(
        vector_mass_ev=vector_mass_ev,
        g_x_ae_max=gx_max,
        g_b_nuclear_max=gb_max,
        g_min_max=min(gx_max, gb_max),
        delta_ae_at_g_021a=delta_ae,
        nuclear_fraction_at_g_021a=nuclear_fraction,
    )


def planar_force_factor() -> float:
    """Return lamellar finite-thickness force factor for the oracle."""

    source = (
        1.0
        - math.exp(
            -SOURCE_LAYER_THICKNESS_IN_LAMBDA
        )
    )

    gap = math.exp(
        -GAP_IN_LAMBDA
    )

    payload_average = (
        1.0
        / PAYLOAD_LAYER_THICKNESS_IN_LAMBDA
        * (
            1.0
            - math.exp(
                -PAYLOAD_LAYER_THICKNESS_IN_LAMBDA
            )
        )
    )

    radial_tail_bound = (
        1.0
        + RADIAL_EDGE_MARGIN_LAMBDA
    ) * math.exp(
        -RADIAL_EDGE_MARGIN_LAMBDA
    )

    return (
        source
        * gap
        * payload_average
        * (
            1.0
            - radial_tail_bound
        )
    )


def required_alpha(range_m: float) -> float:
    """Return equal-magnitude opposite scalar charge needed for 1g."""

    factor = planar_force_factor()

    return math.sqrt(
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


def required_c(
    range_m: float,
    penalty: float,
) -> float:
    """Return inherited material-EFT coefficient target."""

    alpha = required_alpha(
        range_m
    )

    return (
        penalty
        * C_REF
        * alpha
        / ALPHA_ACTIVATED_REF
    )


def max_positive_wilson_curvature(
    a019,
) -> tuple[float, int, float]:
    """Find the largest positive 019A CW curvature on the inherited basin."""

    best_kappa = 0.0
    best_n = -1
    best_rho = float("nan")

    for N in range(3, 17):
        for rho in np.linspace(
            0.25,
            5.0,
            80,
        ):
            value = float(
                a019.cw_curvature_analytic_mp(
                    N,
                    float(rho),
                )
            )

            if (
                math.isfinite(value)
                and value > best_kappa
            ):
                best_kappa = value
                best_n = N
                best_rho = float(rho)

    if best_kappa <= 0.0:
        raise RuntimeError(
            "No positive Wilson curvature found"
        )

    return (
        best_kappa,
        best_n,
        best_rho,
    )


def optimistic_portal_capacity(
    range_m: float,
    vector_mass_ev: float,
    g_min: float,
    kappa_cw: float,
) -> float:
    """Return the deliberately optimistic asymmetric-coupling C_phi ceiling.

    With:
        f = f_max,
        y_P = sqrt(4 pi),
        Hessian exactly at h,
        radial Higgs exactly at vector floor,
        messenger scale chosen to maximize response while reproducing m_phi.

    The algebra reduces to

        C_max =
        (1-h)
        g_min^3
        m_phi^(3/2)
        kappa_CW^(1/4)
        sqrt(f_max)
        /
        M^5.

    This ignores several mandatory effects that can only LOWER the available
    response.  It is therefore an upper bound.
    """

    if g_min <= 0.0:
        return 0.0

    m_phi = HBARC_EV_M / range_m

    return (
        (1.0 - HESSIAN_MIN_FRACTION)
        * g_min**3
        * m_phi**1.5
        * kappa_cw**0.25
        * math.sqrt(MPL_REDUCED_EV)
        / vector_mass_ev**5
    )


def lamellar_stack(
    range_m: float,
) -> tuple[float, float]:
    """Return payload-layer count and total stack height."""

    payload_layer_thickness = (
        PAYLOAD_LAYER_THICKNESS_IN_LAMBDA
        * range_m
    )

    layer_mass = (
        PAYLOAD_DENSITY_KG_M3
        * LAYER_AREA_M2
        * payload_layer_thickness
    )

    layer_count = (
        PAYLOAD_MASS_KG
        / layer_mass
    )

    pitch = (
        CELL_PITCH_IN_LAMBDA
        * range_m
    )

    height = (
        layer_count
        * pitch
    )

    return layer_count, height


def capacity_point(
    range_m: float,
    kappa_cw: float,
) -> CapacityPoint:
    """Construct one optimistic capacity point."""

    # The optimistic capacity always prefers the lowest allowed heavy-vector
    # mass.  Direct constraints are evaluated at that same mass.
    vector_mass = M_VECTOR_MIN_EV

    bounds = direct_vector_bounds(
        vector_mass,
        g_021a=0.75,
    )

    c_max = optimistic_portal_capacity(
        range_m,
        vector_mass,
        bounds.g_min_max,
        kappa_cw,
    )

    c_021a = required_c(
        range_m,
        PENALTY_021A_ISOLATED_FE,
    )

    c_formula = required_c(
        range_m,
        PENALTY_FORMULA_UNIT,
    )

    c_oracle = required_c(
        range_m,
        PENALTY_MULTI_ISOTOPE_ORACLE,
    )

    layers, height = lamellar_stack(
        range_m
    )

    return CapacityPoint(
        range_m=range_m,
        m_phi_ev=HBARC_EV_M / range_m,
        alpha_required=required_alpha(
            range_m
        ),
        c_target_021a=c_021a,
        c_target_formula=c_formula,
        c_target_oracle=c_oracle,
        c_max=c_max,
        deficit_021a=c_021a / max(c_max, 1.0e-300),
        deficit_formula=c_formula / max(c_max, 1.0e-300),
        deficit_oracle=c_oracle / max(c_max, 1.0e-300),
        layer_count=layers,
        stack_height_m=height,
    )


def crossing_range(
    points: list[CapacityPoint],
    attribute: str,
) -> float | None:
    """Interpolate the first deficit=1 crossing in log-log space."""

    values = [
        float(getattr(point, attribute))
        for point in points
    ]

    for left, right, f_left, f_right in zip(
        points[:-1],
        points[1:],
        values[:-1],
        values[1:],
        strict=True,
    ):
        if (
            (f_left - 1.0)
            * (f_right - 1.0)
            <= 0.0
        ):
            x1 = math.log(
                left.range_m
            )
            x2 = math.log(
                right.range_m
            )

            y1 = math.log(
                max(f_left, 1.0e-300)
            )
            y2 = math.log(
                max(f_right, 1.0e-300)
            )

            if abs(y2 - y1) < 1.0e-14:
                return math.exp(
                    0.5 * (x1 + x2)
                )

            x = (
                x1
                + (0.0 - y1)
                * (x2 - x1)
                / (y2 - y1)
            )

            return math.exp(x)

    return None


def power_law_slope(
    points: list[CapacityPoint],
    attribute: str,
    lower_m: float,
    upper_m: float,
) -> float:
    """Fit log(deficit) vs log(range) over one interval."""

    selected = [
        point
        for point in points
        if lower_m <= point.range_m <= upper_m
    ]

    if len(selected) < 3:
        raise RuntimeError(
            "Not enough points for power-law fit"
        )

    x = np.log(
        [
            point.range_m
            for point in selected
        ]
    )

    y = np.log(
        [
            max(
                float(getattr(point, attribute)),
                1.0e-300,
            )
            for point in selected
        ]
    )

    slope, intercept = np.polyfit(
        x,
        y,
        deg=1,
    )

    _ = intercept

    return float(slope)


def main() -> None:
    """Execute the complete 021B0 rerank gate."""

    print(
        "=== 021B0 — CURRENT-KERNEL + DIRECT-VECTOR "
        "+ NANORANGE RERANK GATE ==="
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
        C_LOG,
        "RENORMALIZABLE_VECTOR_HIGGS_MEDIATOR_SECTOR=PASS",
    )
    require_marker(
        R_LOG,
        "020A2R_EXACT_BL_RUNNING_AND_HP_GLOBAL_NATURALNESS_CLOSEOUT=GREEN_NEGATIVE_RESULT",
    )
    require_marker(
        A21_LOG,
        "021A_SHORT_RANGE_ISOTOPE_SIGN_WILSON_VECTOR_PORTAL_GATE=GREEN",
    )
    require_marker(
        A21_LOG,
        "COMPLETE_PROTECTED_MICROSCOPIC_PORTAL_PREFLIGHT=YES_IN_DECLARED_SHORT_RANGE_MODEL",
    )

    if not A21_SOURCE.exists():
        raise RuntimeError(
            f"Missing 021A source: {A21_SOURCE}"
        )

    a21_sha = sha256(
        A21_SOURCE
    )

    print("\n=== UPSTREAM 021A SOURCE AUDIT ===")
    print(
        f"021A_SOURCE_SHA256={a21_sha}"
    )
    print(
        f"021A_EXPECTED_SHA256={EXPECTED_021A_SHA256}"
    )
    print(
        "021A_SOURCE_HASH_MATCH="
        + (
            "PASS"
            if a21_sha == EXPECTED_021A_SHA256
            else "FAIL"
        )
    )

    if a21_sha != EXPECTED_021A_SHA256:
        raise RuntimeError(
            "021A source hash mismatch; audit the actually executed source"
        )

    a019 = load_module(
        "ag021b0_019a",
        A_SOURCE,
    )

    # ------------------------------------------------------------------
    # A. Exact real formula-unit reconstruction.
    # ------------------------------------------------------------------
    print("\n=== A — REAL DINUCLEAR FORMULA-UNIT BOOKKEEPING ===")

    formula = formula_unit()

    print(
        "HOST_FORMULA="
        "Fe2C40H30N16S4"
    )
    print(
        f"FORMULA_ELECTRONS={formula.electrons}"
    )
    print(
        f"FORMULA_BARYONS_FE54={formula.baryons_54}"
    )
    print(
        f"FORMULA_BARYONS_FE58={formula.baryons_58}"
    )
    print(
        "FORMULA_C_OPPOSITE_INTEGRATED_CHARGE="
        f"{formula.c_formula.numerator}/{formula.c_formula.denominator}"
    )
    print(
        "FORMULA_RELATIVE_X_CHARGE="
        f"{formula.relative_charge.numerator}/{formula.relative_charge.denominator}"
    )
    print(
        "FORMULA_NORMALIZATION_PENALTY="
        f"{float(formula.penalty):.15e}"
    )

    exact_expected = (
        formula.electrons == 498
        and formula.baryons_54 == 970
        and formula.baryons_58 == 978
        and formula.c_formula == Fraction(249, 487)
        and formula.relative_charge == Fraction(2, 487)
        and formula.penalty == Fraction(487, 2)
    )

    print(
        "FORMULA_UNIT_RATIONAL_RECONSTRUCTION="
        + (
            "PASS"
            if exact_expected
            else "FAIL"
        )
    )

    # ------------------------------------------------------------------
    # B. Finite-vector kernel sign audit at selected 021A point.
    # ------------------------------------------------------------------
    print("\n=== B — FINITE-VECTOR COMPOSITE-KERNEL SIGN AUDIT ===")

    selected_vector_mass = exact_scalar(
        A21_LOG,
        "SELECTED_VECTOR_MASS_EV=",
    )

    selected_g = exact_scalar(
        A21_LOG,
        "SELECTED_G_BRIDGE=",
    )

    c_formula_float = float(
        formula.c_formula
    )

    q54_upper, bl54, bb54 = fe_site_kernel_upper_bound(
        FE54_A,
        c_formula_float,
        selected_vector_mass,
    )

    q58_upper, bl58, bb58 = fe_site_kernel_upper_bound(
        FE58_A,
        c_formula_float,
        selected_vector_mass,
    )

    print(
        "SELECTED_VECTOR_MASS_EV="
        f"{selected_vector_mass:.15e}"
    )
    print(
        "SELECTED_VECTOR_RANGE_FM="
        f"{vector_range_fm(selected_vector_mass):.15e}"
    )
    print(
        "FE54_BL_KERNEL_ABSOLUTE_UPPER="
        f"{bl54:.15e}"
    )
    print(
        "FE54_BB_KERNEL_CONSERVATIVE_LOWER="
        f"{bb54:.15e}"
    )
    print(
        "FE54_SCALAR_KERNEL_CHARGE_UPPER="
        f"{q54_upper:.15e}"
    )
    print(
        "FE58_BL_KERNEL_ABSOLUTE_UPPER="
        f"{bl58:.15e}"
    )
    print(
        "FE58_BB_KERNEL_CONSERVATIVE_LOWER="
        f"{bb58:.15e}"
    )
    print(
        "FE58_SCALAR_KERNEL_CHARGE_UPPER="
        f"{q58_upper:.15e}"
    )

    formula_kernel_opposite_sign_possible = (
        q54_upper > 0.0
        and q58_upper < 0.0
    )

    both_forced_negative = (
        q54_upper < 0.0
        and q58_upper < 0.0
    )

    print(
        "FORMULA_CORRECTED_FE54_FE58_KERNEL_OPPOSITE_SIGN_POSSIBLE="
        + (
            "YES"
            if formula_kernel_opposite_sign_possible
            else "NO"
        )
    )
    print(
        "FORMULA_CORRECTED_FE_SITE_KERNELS_FORCED_SAME_NEGATIVE_SIGN="
        + (
            "YES"
            if both_forced_negative
            else "NO"
        )
    )

    # Also show the old isolated-Fe c=13/28 assumption, but do not use it to
    # rescue the formula-unit result.
    old_c = 13.0 / 28.0

    old_q54, _, _ = fe_site_kernel_upper_bound(
        FE54_A,
        old_c,
        selected_vector_mass,
    )

    old_q58, _, _ = fe_site_kernel_upper_bound(
        FE58_A,
        old_c,
        selected_vector_mass,
    )

    print(
        "OLD_021A_C_13_OVER_28_FE54_KERNEL_UPPER="
        f"{old_q54:.15e}"
    )
    print(
        "OLD_021A_C_13_OVER_28_FE58_KERNEL_UPPER="
        f"{old_q58:.15e}"
    )
    print(
        "INTEGRATED_CHARGE_SIGN_ALONE_SUFFICIENT_FOR_MATERIAL_SCALAR_SIGN="
        "NO"
    )

    # ------------------------------------------------------------------
    # C. Direct vector ordinary-matter preflight.
    # ------------------------------------------------------------------
    print("\n=== C — DIRECT VECTOR ORDINARY-MATTER PREFLIGHT ===")

    bounds_selected = direct_vector_bounds(
        selected_vector_mass,
        selected_g,
    )

    ae_integral = electron_gminus2_integral(
        selected_vector_mass
    )

    # Small-M analytic check: I -> 1.
    ae_small_mass_relerr = abs(
        ae_integral - 1.0
    )

    print(
        "AE_PREFLIGHT_MAX="
        f"{DELTA_AE_PREFLIGHT_MAX:.15e}"
    )
    print(
        "SELECTED_AE_LOOP_INTEGRAL="
        f"{ae_integral:.15e}"
    )
    print(
        "SELECTED_AE_SMALL_M_LIMIT_RELERR="
        f"{ae_small_mass_relerr:.15e}"
    )
    print(
        "SELECTED_DELTA_AE_AT_G="
        f"{bounds_selected.delta_ae_at_g_021a:.15e}"
    )
    print(
        "SELECTED_G_X_MAX_FROM_LOOSE_AE_PREFLIGHT="
        f"{bounds_selected.g_x_ae_max:.15e}"
    )
    print(
        "SELECTED_G_B_MAX_FROM_100PCT_NUCLEAR_BINDING_PREFLIGHT="
        f"{bounds_selected.g_b_nuclear_max:.15e}"
    )
    print(
        "SELECTED_G_MIN_MAX="
        f"{bounds_selected.g_min_max:.15e}"
    )
    print(
        "SELECTED_NUCLEAR_SELF_ENERGY_FRACTION_AT_G="
        f"{bounds_selected.nuclear_fraction_at_g_021a:.15e}"
    )

    selected_ae_fail = (
        selected_g > bounds_selected.g_x_ae_max
    )

    selected_nuclear_fail = (
        selected_g > bounds_selected.g_b_nuclear_max
    )

    print(
        "021A_SELECTED_DIRECT_X_VECTOR_AE_PREFLIGHT="
        + (
            "FAIL"
            if selected_ae_fail
            else "PASS"
        )
    )
    print(
        "021A_SELECTED_DIRECT_B_VECTOR_NUCLEAR_PREFLIGHT="
        + (
            "FAIL"
            if selected_nuclear_fail
            else "PASS"
        )
    )

    # Scan mass dependence to show whether raising the vector mass can reopen
    # direct coupling before portal M^-5 suppression is applied.
    gmin_best = 0.0
    gmin_best_mass = float("nan")

    for mass in M_VECTOR_AUDIT_GRID_EV:
        bounds = direct_vector_bounds(
            float(mass),
            selected_g,
        )

        if bounds.g_min_max > gmin_best:
            gmin_best = bounds.g_min_max
            gmin_best_mass = float(mass)

    print(
        "DIRECT_VECTOR_AUDIT_BEST_G_MIN_MAX="
        f"{gmin_best:.15e}"
    )
    print(
        "DIRECT_VECTOR_AUDIT_BEST_G_MIN_MASS_EV="
        f"{gmin_best_mass:.15e}"
    )

    # ------------------------------------------------------------------
    # D. Wilson-curvature maximum for optimistic capacity.
    # ------------------------------------------------------------------
    print("\n=== D — OPTIMISTIC WILSON CURVATURE ENVELOPE ===")

    kappa_max, kappa_n, kappa_rho = max_positive_wilson_curvature(
        a019
    )

    print(
        "WILSON_KAPPA_CW_MAX="
        f"{kappa_max:.15e}"
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
        "WILSON_CAPACITY_USES_MAXIMUM_CURVATURE="
        "YES_OPTIMISTIC_UPPER_BOUND"
    )

    # ------------------------------------------------------------------
    # E. Close the original 021A scalar-range window.
    # ------------------------------------------------------------------
    print("\n=== E — OLD 021A RANGE ASYMMETRIC-COUPLING CAPACITY ===")

    old_points = [
        capacity_point(
            float(value),
            kappa_max,
        )
        for value in OLD_RANGE_GRID
    ]

    best_old_021a = min(
        old_points,
        key=lambda point: point.deficit_021a,
    )

    best_old_formula = min(
        old_points,
        key=lambda point: point.deficit_formula,
    )

    best_old_oracle = min(
        old_points,
        key=lambda point: point.deficit_oracle,
    )

    print(
        "OLD_RANGE_BEST_021A_ASSUMPTION_RANGE_M="
        f"{best_old_021a.range_m:.15e}"
    )
    print(
        "OLD_RANGE_BEST_021A_ASSUMPTION_DEFICIT="
        f"{best_old_021a.deficit_021a:.15e}"
    )
    print(
        "OLD_RANGE_BEST_FORMULA_RANGE_M="
        f"{best_old_formula.range_m:.15e}"
    )
    print(
        "OLD_RANGE_BEST_FORMULA_DEFICIT="
        f"{best_old_formula.deficit_formula:.15e}"
    )
    print(
        "OLD_RANGE_BEST_ORACLE_RANGE_M="
        f"{best_old_oracle.range_m:.15e}"
    )
    print(
        "OLD_RANGE_BEST_ORACLE_DEFICIT="
        f"{best_old_oracle.deficit_oracle:.15e}"
    )

    old_range_closed = (
        best_old_oracle.deficit_oracle > 1.0
    )

    print(
        "021A_100UM_TO_10CM_DIRECT_VECTOR_PORTAL="
        + (
            "CLOSED_EVEN_UNDER_OPTIMISTIC_ISOTOPE_ORACLE"
            if old_range_closed
            else "RETAINS_CAPACITY_POINT"
        )
    )

    # ------------------------------------------------------------------
    # F. Nanorange capacity oracle.
    # ------------------------------------------------------------------
    print("\n=== F — NANOLAMELLAR CAPACITY ORACLE ===")

    nano_points = [
        capacity_point(
            float(value),
            kappa_max,
        )
        for value in NANO_RANGE_GRID
    ]

    crossing_021a = crossing_range(
        nano_points,
        "deficit_021a",
    )

    crossing_formula = crossing_range(
        nano_points,
        "deficit_formula",
    )

    crossing_oracle = crossing_range(
        nano_points,
        "deficit_oracle",
    )

    best_nano_oracle = min(
        nano_points,
        key=lambda point: point.deficit_oracle,
    )

    best_nano_formula = min(
        nano_points,
        key=lambda point: point.deficit_formula,
    )

    slope_oracle = power_law_slope(
        nano_points,
        "deficit_oracle",
        1.0e-9,
        1.0e-6,
    )

    print(
        "NANO_BEST_ORACLE_RANGE_M="
        f"{best_nano_oracle.range_m:.15e}"
    )
    print(
        "NANO_BEST_ORACLE_DEFICIT="
        f"{best_nano_oracle.deficit_oracle:.15e}"
    )
    print(
        "NANO_BEST_FORMULA_RANGE_M="
        f"{best_nano_formula.range_m:.15e}"
    )
    print(
        "NANO_BEST_FORMULA_DEFICIT="
        f"{best_nano_formula.deficit_formula:.15e}"
    )
    print(
        "NANO_DEFICIT_POWER_LAW_SLOPE="
        f"{slope_oracle:.15e}"
    )

    def print_crossing(
        name: str,
        value: float | None,
    ) -> None:
        if value is None:
            print(
                f"{name}=NONE_IN_SCAN"
            )
        else:
            layers, height = lamellar_stack(
                value
            )

            print(
                f"{name}={value:.15e}"
            )
            print(
                f"{name}_LAYERS={layers:.15e}"
            )
            print(
                f"{name}_STACK_HEIGHT_M={height:.15e}"
            )

    print_crossing(
        "NANO_CROSSING_021A_ASSUMPTION_M",
        crossing_021a,
    )

    print_crossing(
        "NANO_CROSSING_FORMULA_NORMALIZATION_M",
        crossing_formula,
    )

    print_crossing(
        "NANO_CROSSING_OPTIMISTIC_ORACLE_M",
        crossing_oracle,
    )

    nano_capacity_survives = (
        crossing_oracle is not None
        or best_nano_oracle.deficit_oracle <= 1.0
    )

    print(
        "NANOLAMELLAR_SCALING_ESCAPE="
        + (
            "SUPPORTED_AS_CAPACITY_PREFLIGHT"
            if nano_capacity_survives
            else "NOT_FOUND"
        )
    )

    # ------------------------------------------------------------------
    # G. Selected nanorange oracle point detail.
    # ------------------------------------------------------------------
    print("\n=== G — BEST NANORANGE ORACLE DETAIL ===")

    best = best_nano_oracle

    bounds_floor = direct_vector_bounds(
        M_VECTOR_MIN_EV,
        selected_g,
    )

    print(
        "BEST_NANO_RANGE_M="
        f"{best.range_m:.15e}"
    )
    print(
        "BEST_NANO_M_PHI_EV="
        f"{best.m_phi_ev:.15e}"
    )
    print(
        "BEST_NANO_ALPHA_REQUIRED="
        f"{best.alpha_required:.15e}"
    )
    print(
        "BEST_NANO_C_TARGET_ORACLE="
        f"{best.c_target_oracle:.15e}"
    )
    print(
        "BEST_NANO_C_MAX_OPTIMISTIC="
        f"{best.c_max:.15e}"
    )
    print(
        "BEST_NANO_DEFICIT_ORACLE="
        f"{best.deficit_oracle:.15e}"
    )
    print(
        "BEST_NANO_G_X_MAX="
        f"{bounds_floor.g_x_ae_max:.15e}"
    )
    print(
        "BEST_NANO_G_B_MAX="
        f"{bounds_floor.g_b_nuclear_max:.15e}"
    )
    print(
        "BEST_NANO_G_MIN_MAX="
        f"{bounds_floor.g_min_max:.15e}"
    )
    print(
        "BEST_NANO_LAYER_COUNT="
        f"{best.layer_count:.15e}"
    )
    print(
        "BEST_NANO_STACK_HEIGHT_M="
        f"{best.stack_height_m:.15e}"
    )

    # ------------------------------------------------------------------
    # H. Blind wildcard diagnostics — not evidence.
    # ------------------------------------------------------------------
    print("\n=== BLIND WILDCARD DIAGNOSTICS — NOT EVIDENCE ===")

    reference_range = (
        crossing_oracle
        if crossing_oracle is not None
        else best.range_m
    )

    for factor in BLIND_WILDCARDS:
        test_range = min(
            max(
                reference_range * factor,
                NANO_RANGE_MIN_M,
            ),
            OLD_RANGE_MAX_M,
        )

        point = capacity_point(
            test_range,
            kappa_max,
        )

        print(
            f"WILDCARD_FACTOR={factor:.6f} "
            f"RANGE_M={test_range:.9e} "
            f"ORACLE_DEFICIT={point.deficit_oracle:.9e} "
            f"FORMULA_DEFICIT={point.deficit_formula:.9e} "
            f"LAYERS={point.layer_count:.9e}"
        )

    print(
        "BLIND_WILDCARD_VALUES_USED_AS_EVIDENCE=NO"
    )

    # ------------------------------------------------------------------
    # I. Final fail-closed decision.
    # ------------------------------------------------------------------
    print("\n=== 021B0 DECISION ===")

    source_hash_pass = (
        a21_sha == EXPECTED_021A_SHA256
    )

    formula_pass = exact_expected

    kernel_invalidates_021a_sign = (
        both_forced_negative
    )

    selected_direct_vector_fail = (
        selected_ae_fail
        or selected_nuclear_fail
    )

    old_window_fail = old_range_closed

    validation_pass = (
        source_hash_pass
        and formula_pass
        and ae_small_mass_relerr < 0.05
    )

    if not validation_pass:
        print(
            "021B0_CURRENT_KERNEL_DIRECT_VECTOR_AND_NANORANGE_RERANK_GATE="
            "RED_VALIDATION_FAILURE"
        )
        print(
            "NEXT=DEBUG_VALIDATION_BEFORE_SCIENTIFIC_INTERPRETATION"
        )

    elif (
        kernel_invalidates_021a_sign
        and selected_direct_vector_fail
        and old_window_fail
        and nano_capacity_survives
    ):
        print(
            "021B0_CURRENT_KERNEL_DIRECT_VECTOR_AND_NANORANGE_RERANK_GATE="
            "GREEN_NEGATIVE_WITH_NANORANGE_ESCAPE"
        )
        print(
            "021A_70_PERCENT_PROMOTION="
            "REJECTED_BY_POST_RUN_CLAIM_AUDIT"
        )
        print(
            "021A_ISOLATED_FE_INTEGRATED_CHARGE_SIGN="
            "NOT_VALID_FOR_COMPLETE_FORMULA_UNIT_KERNEL"
        )
        print(
            "FORMULA_UNIT_FINITE_KERNEL_FE54_FE58_OPPOSITE_SIGN="
            "REJECTED_AT_SELECTED_VECTOR_MASS"
        )
        print(
            "021A_SELECTED_DIRECT_VECTOR_ORDINARY_MATTER_PREFLIGHT="
            "FAIL"
        )
        print(
            "021A_100UM_TO_10CM_WINDOW="
            "CLOSED_EVEN_UNDER_OPTIMISTIC_CAPACITY_BOUND"
        )
        print(
            "NANOLAMELLAR_SCALING_ESCAPE="
            "SUPPORTED_AS_CAPACITY_PREFLIGHT"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY"
        )
        print(
            "HEURISTIC_CHANGE="
            "NONE_CAPACITY_PREFLIGHT_IS_NOT_MICROSCOPIC_REALIZATION"
        )
        print(
            "NEXT="
            "022A_NANOLAMELLAR_KERNEL_LEVEL_SIGN_AND_COMPLETE_PORTAL_GATE"
        )

    elif (
        kernel_invalidates_021a_sign
        and selected_direct_vector_fail
        and old_window_fail
        and not nano_capacity_survives
    ):
        print(
            "021B0_CURRENT_KERNEL_DIRECT_VECTOR_AND_NANORANGE_RERANK_GATE="
            "GREEN_NEGATIVE_RESULT"
        )
        print(
            "021A_70_PERCENT_PROMOTION="
            "REJECTED"
        )
        print(
            "DIRECT_VECTOR_SHORT_RANGE_BRANCH="
            "CLOSED_IN_TESTED_CAPACITY_CLASS"
        )
        print(
            "NANOLAMELLAR_SCALING_ESCAPE="
            "NOT_FOUND"
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
            "GLOBAL_RERANK_TO_INTRINSICALLY_STABLE_GR_OR_OTHER_NEW_PROTECTION_PRINCIPLE"
        )

    else:
        print(
            "021B0_CURRENT_KERNEL_DIRECT_VECTOR_AND_NANORANGE_RERANK_GATE="
            "INCOMPLETE_OR_SURVIVING_021A_ASSUMPTION"
        )
        print(
            "NEXT="
            "INSPECT_SURVIVING_CONDITION_BEFORE_ESCALATION"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY"
        )

    # Permanent claim boundaries.
    print(
        "NANOLAMELLAR_REAL_MATERIAL="
        "NOT_ESTABLISHED"
    )
    print(
        "EXACT_2026_DIRECT_VECTOR_EXPERIMENTAL_CLOSURE="
        "NOT_ESTABLISHED_BY_THIS_PREFLIGHT"
    )
    print(
        "COMPLETE_MOLECULAR_KERNEL="
        "NOT_ESTABLISHED"
    )
    print(
        "COMPLETE_MICROSCOPIC_NANOLAMELLAR_PORTAL="
        "NO"
    )
    print(
        "REAL_ANTIGRAVITY_MATERIAL="
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

    # Preserve prior durable results.
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
        "019B_ANOMALY_FREE_VECTOR_CURRENT_RESULT="
        "RETAINED"
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
        "RETAINED_BUT_PROMOTION_REAUDITED"
    )
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_021B0_CURRENT_KERNEL_DIRECT_VECTOR_AND_NANORANGE_RERANK_GATE"
    )


if __name__ == "__main__":
    main()
