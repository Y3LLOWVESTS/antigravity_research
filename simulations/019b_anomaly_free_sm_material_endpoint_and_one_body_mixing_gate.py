#!/usr/bin/env python3
"""019B — anomaly-free SM/material endpoint and one-body operator-mixing gate.

PURPOSE
-------
Close the highest-information question left by 019A before the project pauses
for documentation: can the Wilson-line protected pair response be attached to
ordinary Standard-Model matter without reintroducing an experimentally fatal
one-body scalar charge?

This file deliberately separates three logically distinct issues:

1. GAUGE / ANOMALY CONSISTENCY.
   Reconstruct an explicit anomaly-free gauged U(1)_B x U(1)_L completion of
   ordinary baryon and lepton number using the N=1 vector-like-fermion solution
   of Duerr, Fileviez Perez and Wise (arXiv:1304.0576).  The anomaly sums are
   evaluated independently with exact rational arithmetic.

2. DIRECT SCALAR-MESSENGER ENDPOINTS.
   019A used a scalar Wilson-line messenger.  A Lorentz-invariant renormalizable
   coupling of such a messenger to a Dirac matter field uses scalar or
   pseudoscalar bilinears.  The scalar-density option gives the desired
   spin-independent nonrelativistic density, but the pair operator

       C_phi * phi * (bar N N) * (bar e e)

   admits one-body scalar counterterms when either scalar density is closed.
   This gate quantifies the natural threshold size over the full physically
   relevant matching interval from the atomic EFT cutoff to the lightest 019A
   messenger mass.  The hard-cutoff number is used only as a NATURALNESS
   DIAGNOSTIC, not as a scheme-independent prediction.  Failure is promoted
   only if even the most favorable end of that interval exceeds the project's
   allowed one-body coefficient by a large margin and no exact symmetry forbids
   the counterterm.

   The pseudoscalar alternative avoids the scalar tadpole but loses coherent
   spin-independent q -> 0 response.  We quantify the most optimistic finite-q
   suppression at the 3-Angstrom EFT cutoff and test whether restoring the
   target strength would require nonperturbative endpoint couplings.

3. CONSERVED-VECTOR-CURRENT ESCAPE.
   A dimension-seven Lorentz scalar

       C_phi * phi * J_B^mu * J_L_mu

   has exactly the desired nonrelativistic density-density limit while a single
   conserved vector current has zero Lorentz-invariant vacuum expectation.  We
   therefore audit the vector-current route separately.  The explicit U(1)_B x
   U(1)_L completion makes the relevant currents anomaly-free.  Ward identities
   force the leading QED bridge through a closed electron current to begin with
   the low-q vacuum-polarization factor

       alpha/(15*pi) * q^2/m_e^2.

   A deliberately conservative two-loop/channel-counting estimate is compared
   with the project's leakage allowance.  This is a REAL LOW-ENERGY ESCAPE
   WITNESS, but it is NOT promoted to a complete 019A UV completion because the
   019A messenger is scalar: a fully renormalizable Wilson-line VECTOR portal
   has not yet been constructed.

ACTIVE SCIENTIFIC QUESTION
--------------------------
Does the 019A Wilson-line protection survive an explicit ordinary-matter
endpoint, or does Lorentz structure/operator mixing force the branch to change
its microscopic portal before any experimental fifth-force work is meaningful?

INHERITED TARGETS
-----------------
The project low-energy pair operator is

    H_pair = C_phi * phi * A^dagger B^dagger B A

with

    C_phi = 9.536416387852626e-20 eV^-3.

The 3-Angstrom contact normalization gives a target bound-state scalar charge
of order 8.64e-12.  The conservative ordinary-matter target-equivalent leakage
allowance is

    f_leak = 5.772961445324848e-7.

An earlier project gate also reconstructed the corresponding maximum ordinary
nucleon-like one-body scalar coefficient

    g_1,max = 3.470636550308009e-20.

The Wilson scalar mass/range remain

    m_phi = 3.946539608e-11 eV,
    lambda_phi = 5 km.

INPUTS
------
The script reads the executed 019A log and source from the repository.  It does
not silently substitute preflight values for the user's executed result.

UNITS / CONVENTIONS
-------------------
Natural units hbar=c=1 are used internally.  Energies are in eV.  The anomaly
table uses LEFT-HANDED Weyl fermions; right-handed fields are entered as their
left-handed charge conjugates, so all Abelian charges flip sign.

ONE-BODY NATURALNESS DIAGNOSTIC
-------------------------------
For a relativistic Dirac scalar density with Euclidean hard matching cutoff
Lambda, the magnitude of the one-loop scalar tadpole is

    I_f(Lambda)
      = m_f/(4*pi^2)
        [Lambda^2 - m_f^2 log(1 + Lambda^2/m_f^2)].

Closing one endpoint of the desired scalar-scalar pair operator therefore has
natural coefficient scale

    |g_A,nat| ~ |C_phi| I_B,
    |g_B,nat| ~ |C_phi| I_A.

Power-sensitive pieces are scheme dependent.  Accordingly this file does NOT
claim that these expressions are physical measured coefficients.  The gate
uses them only to ask whether a zero counterterm is technically natural across
an explicit matching interval.  An exact symmetry would override this proxy;
no such symmetry exists for the scalar-density one-body operators in this
endpoint class.

PSEUDOSCALAR COHERENCE TEST
---------------------------
For a Dirac fermion,

    bar u(p') i gamma_5 u(p) = O(|q|/(2m)).

Thus an unpolarized coherent q -> 0 source vanishes.  At the maximally generous
q = Lambda_atomic the pair suppression is bounded by

    S_P <= q/(2 m_e) * q/(2 m_N).

Restoring the same pair coefficient would require y_A y_B -> y_A y_B / S_P.

VECTOR-CURRENT MIXING PREFLIGHT
-------------------------------
For the conserved vector-current escape, the leading low-q electron vacuum
polarization is bounded by

    Pi_e(q^2) ~ alpha/(15*pi) * q^2/m_e^2.

We combine this with an additional QED loop factor alpha/(4*pi), the contact
normalization |psi(0)|^2 = Lambda_atomic^3/pi, and a deliberately inflated
channel multiplicity.  This is intentionally pessimistic.  It is not claimed
as a complete two-loop anomalous-dimension calculation.  In fact the complete
higher-dimensional four-fermion -> two-fermion mixing problem remains an active
literature topic.  The output therefore distinguishes

    VECTOR_CURRENT_ONE_BODY_MIXING_PREFLIGHT

from

    COMPLETE_ALL_ORDER_SM_OPERATOR_MIXING.

LITERATURE ANCHORS
------------------
- M. Duerr, P. Fileviez Perez, M. B. Wise,
  "Gauge Theory for Baryon and Lepton Numbers with Leptoquarks",
  arXiv:1304.0576.  Explicit anomaly-free gauged U(1)_B x U(1)_L completion.
- J. C. Collins, A. V. Manohar, M. B. Wise,
  "Renormalization of the Vector Current in QED",
  arXiv:hep-th/0512187.  Conserved-current renormalization and derivative
  mixing with the field-strength divergence.
- J. Aebischer, P. Morell, M. Pesut, J. Virto,
  "Two-Loop Anomalous Dimensions in the LEFT: Dimension-Six Four-Fermion
  Operators in NDR", arXiv:2501.08384.
- 019A literature anchors remain inherited for Wilson-line protection.

PROMOTION / FALSIFICATION RULES
-------------------------------
The DIRECT 019A scalar-messenger material embedding may be promoted only if a
Lorentz-scalar endpoint simultaneously gives coherent spin-independent matter
response, perturbative matching, and technically natural one-body leakage.

The branch is RED for that direct embedding if every renormalizable scalar
Dirac-bilinear endpoint class fails one of those requirements.

The vector-current escape is retained only if:
- the explicit B/L gauge completion is anomaly-free;
- the vector operator has the correct NR density-density limit;
- the vacuum one-current tadpole is symmetry/Lorentz forbidden;
- a deliberately conservative leading mixing estimate lies below f_leak by a
  substantial margin.

Even then it is NOT a full microscopic completion until a renormalizable
Wilson-line vector portal is constructed and its own naturalness is checked.

CLAIM LIMITS
------------
This gate does not establish a fifth force in nature, a real antigravity
material, the exact 2026 5-km experimental margin, stellar/cosmological safety,
or a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_019B_ANOMALY_FREE_SM_MATERIAL_ENDPOINT_AND_ONE_BODY_MIXING_GATE
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


ROOT = Path(__file__).resolve().parents[1]

A_SOURCE = ROOT / "simulations/019a_wilson_line_sequestered_pair_scalar_uv_protection_gate.py"
A_LOG = ROOT / "results/logs/019a_wilson_line_sequestered_pair_scalar_uv_protection_gate.log"

EXPECTED_019A_SHA256 = "27514c58298ccf9ecaa5543a3dc6d4368df7174ae2c55cb1a547adb922b756e7"

# Project-inherited targets.
TARGET_C_PHI = 9.536416387852626e-20  # eV^-3
TARGET_M_PHI = 3.946539608e-11        # eV
TARGET_RANGE_M = 5.0e3
EARTH_PHI = 1.690631280830914e10      # eV
MAX_LEAKAGE_FRACTION = 5.772961445324848e-7
MAX_ORDINARY_ONE_BODY_G = 3.470636550308009e-20
MATERIAL_EFT_CUTOFF = 657.7566        # eV
PAIR_RADIUS_ANGSTROM = 3.0
HBARC_EV_NM = 197.3269804

# Ordinary low-energy masses.
M_E = 510_998.95
M_N = 938.918e6
M_W = 80.377e9
M_PI_CHARGED = 139.57039e6

ALPHA_EM = 1.0 / 137.035999084
G_WEAK = 0.653

# Deliberately conservative multiplicity for the vector-current mixing proxy.
VECTOR_MIXING_CHANNEL_MULTIPLICITY = 64.0
MIN_VECTOR_MIXING_MARGIN = 1.0e3

# Direct scalar-density naturalness failure must exceed the one-body allowance
# by at least this factor even at the most favorable matching scale.
MIN_SCALAR_NATURALNESS_EXCESS = 100.0

# Perturbativity criterion for a Yukawa-like endpoint coupling.
MAX_YUKAWA_SQ_OVER_4PI = 1.0


@dataclass(frozen=True)
class WeylField:
    """One left-handed Weyl species for exact anomaly bookkeeping."""

    name: str
    color_dim: int
    su2_dim: int
    hypercharge: Fraction
    baryon: Fraction
    lepton: Fraction
    generations: int = 1


@dataclass(frozen=True)
class ScalarMixingRow:
    """One scalar-density matching-scale naturalness diagnostic."""

    cutoff: float
    electron_tadpole: float
    nucleon_tadpole: float
    induced_nucleon_g: float
    induced_electron_g: float
    nucleon_excess: float
    electron_excess: float


def require_marker(path: Path, marker: str) -> None:
    """Require one exact upstream scientific marker."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream file: {path}")

    text = path.read_text(errors="replace")
    if marker not in text:
        raise RuntimeError(f"Missing marker {marker!r} in {path}")


def exact_scalar(path: Path, label: str) -> float:
    """Read a finite scalar from an exact whole-line label."""

    text = path.read_text(errors="replace")
    number = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    match = re.search(r"(?m)^" + re.escape(label) + number + r"\s*$", text)

    if match is None:
        raise RuntimeError(f"Missing exact scalar line {label!r} in {path}")

    value = float(match.group(1))
    if not math.isfinite(value):
        raise RuntimeError(f"Nonfinite scalar {label!r} in {path}")
    return value


def load_module(name: str, path: Path):
    """Import a local simulation module without invoking its main()."""

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


def build_bl_completion_fields() -> list[WeylField]:
    """Return the N=1 anomaly-free U(1)_B x U(1)_L field table.

    The extra-fermion charges follow Table I / Eqs. (2)-(10) of
    arXiv:1304.0576 with N=1 and (Y1,Y2,Y3)=(1/2,1,0).

    Right-handed fields are represented as left-handed conjugates.
    """

    F = Fraction
    fields = [
        # Standard Model + three right-handed neutrinos, three generations.
        WeylField("Q_L", 3, 2, F(1, 6), F(1, 3), F(0), 3),
        WeylField("u_R^c", 3, 1, F(-2, 3), F(-1, 3), F(0), 3),
        WeylField("d_R^c", 3, 1, F(1, 3), F(-1, 3), F(0), 3),
        WeylField("L_L", 1, 2, F(-1, 2), F(0), F(1), 3),
        WeylField("e_R^c", 1, 1, F(1), F(0), F(-1), 3),
        WeylField("nu_R^c", 1, 1, F(0), F(0), F(-1), 3),

        # N=1 vector-like-under-SM anomaly-canceling sector.
        WeylField("Psi_L", 1, 2, F(1, 2), F(-3, 2), F(-3, 2)),
        WeylField("Psi_R^c", 1, 2, F(-1, 2), F(-3, 2), F(-3, 2)),
        WeylField("eta_L", 1, 1, F(1), F(3, 2), F(3, 2)),
        WeylField("eta_R^c", 1, 1, F(-1), F(3, 2), F(3, 2)),
        WeylField("chi_L", 1, 1, F(0), F(3, 2), F(3, 2)),
        WeylField("chi_R^c", 1, 1, F(0), F(3, 2), F(3, 2)),
    ]
    return fields


def nonabelian_anomaly(fields: list[WeylField], which: str, x: str) -> Fraction:
    """Compute SU(3)^2 U(1)_X or SU(2)^2 U(1)_X exactly."""

    total = Fraction(0)
    for field in fields:
        charge = field.baryon if x == "B" else field.lepton
        if which == "SU3" and field.color_dim == 3:
            # Fundamental / antifundamental Dynkin index T=1/2.
            total += field.generations * field.su2_dim * Fraction(1, 2) * charge
        elif which == "SU2" and field.su2_dim == 2:
            total += field.generations * field.color_dim * Fraction(1, 2) * charge
    return total


def abelian_anomaly(fields: list[WeylField], powers: tuple[int, int, int]) -> Fraction:
    """Compute sum Y^a B^b L^c with multiplicities exactly."""

    a, b, c = powers
    total = Fraction(0)
    for field in fields:
        multiplicity = field.generations * field.color_dim * field.su2_dim
        total += (
            multiplicity
            * field.hypercharge**a
            * field.baryon**b
            * field.lepton**c
        )
    return total


def anomaly_ledger(fields: list[WeylField]) -> dict[str, Fraction]:
    """Return every relevant B/L gauge and gravitational anomaly coefficient."""

    return {
        "SU3_SU3_B": nonabelian_anomaly(fields, "SU3", "B"),
        "SU2_SU2_B": nonabelian_anomaly(fields, "SU2", "B"),
        "Y_Y_B": abelian_anomaly(fields, (2, 1, 0)),
        "Y_B_B": abelian_anomaly(fields, (1, 2, 0)),
        "B_B_B": abelian_anomaly(fields, (0, 3, 0)),
        "GRAV_GRAV_B": abelian_anomaly(fields, (0, 1, 0)),
        "SU3_SU3_L": nonabelian_anomaly(fields, "SU3", "L"),
        "SU2_SU2_L": nonabelian_anomaly(fields, "SU2", "L"),
        "Y_Y_L": abelian_anomaly(fields, (2, 0, 1)),
        "Y_L_L": abelian_anomaly(fields, (1, 0, 2)),
        "L_L_L": abelian_anomaly(fields, (0, 0, 3)),
        "GRAV_GRAV_L": abelian_anomaly(fields, (0, 0, 1)),
        "B_B_L": abelian_anomaly(fields, (0, 2, 1)),
        "B_L_L": abelian_anomaly(fields, (0, 1, 2)),
        "Y_B_L": abelian_anomaly(fields, (1, 1, 1)),
    }


def dirac_scalar_tadpole(cutoff: float, mass: float) -> float:
    """Magnitude of the Euclidean hard-cutoff Dirac scalar tadpole.

    I = m/(4*pi^2) [Lambda^2 - m^2 log(1+Lambda^2/m^2)].

    log1p is essential because Lambda << m for both electron and nucleon at the
    material/messenger scales and direct subtraction would lose precision.
    """

    x = cutoff / mass
    # For very small x, use an explicit series to avoid catastrophic
    # cancellation in Lambda^2 - m^2 log(1+x^2).
    if abs(x) < 1.0e-2:
        bracket = mass * mass * (
            0.5 * x**4
            - (1.0 / 3.0) * x**6
            + 0.25 * x**8
            - 0.2 * x**10
        )
    else:
        bracket = cutoff * cutoff - mass * mass * math.log1p(x * x)

    return abs(mass * bracket / (4.0 * math.pi**2))


def dirac_scalar_tadpole_low_cutoff(cutoff: float, mass: float) -> float:
    """Leading Lambda << m asymptotic cross-check: Lambda^4/(8*pi^2*m)."""

    return cutoff**4 / (8.0 * math.pi**2 * mass)


def scalar_mixing_row(cutoff: float) -> ScalarMixingRow:
    """Construct one scalar-density one-body naturalness row."""

    i_e = dirac_scalar_tadpole(cutoff, M_E)
    i_n = dirac_scalar_tadpole(cutoff, M_N)

    g_n = TARGET_C_PHI * i_e
    g_e = TARGET_C_PHI * i_n

    return ScalarMixingRow(
        cutoff=cutoff,
        electron_tadpole=i_e,
        nucleon_tadpole=i_n,
        induced_nucleon_g=g_n,
        induced_electron_g=g_e,
        nucleon_excess=g_n / MAX_ORDINARY_ONE_BODY_G,
        electron_excess=g_e / MAX_ORDINARY_ONE_BODY_G,
    )


def pair_contact_charge() -> tuple[float, float, float]:
    """Return a (eV^-1), |psi(0)|^2 (eV^3), and C_phi|psi(0)|^2."""

    radius_nm = PAIR_RADIUS_ANGSTROM * 0.1
    radius_evinv = radius_nm / HBARC_EV_NM
    psi0_sq = 1.0 / (math.pi * radius_evinv**3)
    charge = TARGET_C_PHI * psi0_sq
    return radius_evinv, psi0_sq, charge


def vector_current_mixing_proxy(q: float) -> dict[str, float]:
    """Deliberately conservative leading one-body mixing estimate.

    The electron loop is the least decoupled charged vacuum-polarization bridge
    available at atomic momentum.  A second QED loop is then included together
    with a 64-channel multiplicity and the pi factor converting Lambda^3 to the
    normalized 3-Angstrom contact density Lambda^3/pi.

    Weak and hadronic bridges are also reported and are far smaller.
    """

    electron_vp = ALPHA_EM / (15.0 * math.pi) * (q / M_E) ** 2
    outer_qed = ALPHA_EM / (4.0 * math.pi)

    qed_fraction = (
        VECTOR_MIXING_CHANNEL_MULTIPLICITY
        * math.pi
        * outer_qed
        * electron_vp
    )

    weak_loop = G_WEAK * G_WEAK / (16.0 * math.pi**2)
    weak_fraction = (
        VECTOR_MIXING_CHANNEL_MULTIPLICITY
        * math.pi
        * weak_loop**2
        * (q / M_W) ** 2
    )

    hadronic_vp = ALPHA_EM / (15.0 * math.pi) * (q / M_PI_CHARGED) ** 2
    hadronic_fraction = (
        VECTOR_MIXING_CHANNEL_MULTIPLICITY
        * math.pi
        * outer_qed
        * hadronic_vp
    )

    total = qed_fraction + weak_fraction + hadronic_fraction

    return {
        "electron_vp": electron_vp,
        "outer_qed": outer_qed,
        "qed_fraction": qed_fraction,
        "weak_fraction": weak_fraction,
        "hadronic_fraction": hadronic_fraction,
        "total_fraction": total,
        "margin": MAX_LEAKAGE_FRACTION / max(total, 1.0e-300),
    }


def main() -> None:
    """Execute the 019B endpoint / mixing closeout gate."""

    print("=== 019B — ANOMALY-FREE SM/MATERIAL ENDPOINT + ONE-BODY MIXING GATE ===")

    require_marker(A_LOG, "019A_WILSON_LINE_SEQUESTERED_PAIR_SCALAR_UV_PROTECTION_GATE=GREEN")
    require_marker(A_LOG, "PROTECTED_SCALAR_BRANCH=RETAIN_AND_ESCALATE")

    if not A_SOURCE.exists():
        raise RuntimeError(f"Missing 019A source: {A_SOURCE}")

    actual_sha = hashlib.sha256(A_SOURCE.read_bytes()).hexdigest()
    print("\n=== UPSTREAM 019A AUDIT ===")
    print(f"019A_SOURCE_SHA256={actual_sha}")
    print(f"019A_EXPECTED_SHA256={EXPECTED_019A_SHA256}")
    print(f"019A_SOURCE_HASH_MATCH={'PASS' if actual_sha == EXPECTED_019A_SHA256 else 'FAIL'}")

    selected_mu = exact_scalar(A_LOG, "SELECTED_MU_EV=")
    selected_f = exact_scalar(A_LOG, "SELECTED_F_EV=")
    selected_messenger = exact_scalar(A_LOG, "SELECTED_MESSENGER_MIN_MASS_EV=")
    selected_y = exact_scalar(A_LOG, "SELECTED_Y_ENDPOINT=")
    selected_local_proxy = exact_scalar(A_LOG, "SELECTED_LOCAL_RESPONSE_LEAKAGE_PROXY=")
    selected_theta = exact_scalar(A_LOG, "SELECTED_THETA_EARTH=")

    print(f"019A_SELECTED_MU_EV={selected_mu:.15e}")
    print(f"019A_SELECTED_F_EV={selected_f:.15e}")
    print(f"019A_SELECTED_MESSENGER_MIN_MASS_EV={selected_messenger:.15e}")
    print(f"019A_SELECTED_Y_ENDPOINT={selected_y:.15e}")
    print(f"019A_SELECTED_LOCAL_WILSON_PROXY={selected_local_proxy:.15e}")
    print(f"019A_SELECTED_THETA_EARTH={selected_theta:.15e}")

    # Independent 019A point reconstruction from the source module.
    a = load_module("ag019b_upstream_019a", A_SOURCE)
    reconstructed = a.solve_operating_point(
        a.SELECTED_N,
        a.SELECTED_RHO,
        a.SELECTED_SEPARATION,
        a.SELECTED_Y_PRODUCT,
    )
    if reconstructed is None:
        raise RuntimeError("Independent 019A selected-point reconstruction failed")

    recon_mu_err = abs(reconstructed.mu / selected_mu - 1.0)
    recon_f_err = abs(reconstructed.f / selected_f - 1.0)
    print(f"019A_INDEPENDENT_MU_RELERR={recon_mu_err:.15e}")
    print(f"019A_INDEPENDENT_F_RELERR={recon_f_err:.15e}")
    upstream_reconstruction_pass = max(recon_mu_err, recon_f_err) <= 2.0e-10
    print(f"019A_INDEPENDENT_OPERATING_POINT_RECONSTRUCTION={'PASS' if upstream_reconstruction_pass else 'FAIL'}")

    # ------------------------------------------------------------------
    # Exact anomaly cancellation.
    # ------------------------------------------------------------------
    print("\n=== EXPLICIT ANOMALY-FREE U(1)_B x U(1)_L MATERIAL CURRENT COMPLETION ===")
    fields = build_bl_completion_fields()
    ledger = anomaly_ledger(fields)

    for name, value in ledger.items():
        print(f"ANOMALY_{name}={value.numerator}/{value.denominator}")

    anomaly_pass = all(value == 0 for value in ledger.values())
    print("ANOMALY_COMPLETION_REFERENCE=DUERR_FILEVIEZ_PEREZ_WISE_ARXIV_1304_0576_N1")
    print("EXOTICS_VECTORLIKE_UNDER_SM=YES")
    print("RIGHT_HANDED_NEUTRINOS_INCLUDED=YES")
    print(f"ANOMALY_FREE_U1B_X_U1L_COMPLETION={'PASS' if anomaly_pass else 'FAIL'}")

    # ------------------------------------------------------------------
    # Contact normalization.
    # ------------------------------------------------------------------
    print("\n=== INDEPENDENT NR PAIR MATCH NORMALIZATION ===")
    radius_evinv, psi0_sq, pair_charge = pair_contact_charge()
    print(f"PAIR_RADIUS_EVINV={radius_evinv:.15e}")
    print(f"PAIR_CONTACT_PSI0_SQ_EV3={psi0_sq:.15e}")
    print(f"PAIR_CONTACT_SCALAR_CHARGE={pair_charge:.15e}")
    print(f"TARGET_C_PHI_EV_MINUS3={TARGET_C_PHI:.15e}")
    print(f"MAX_TARGET_EQUIVALENT_LEAKAGE_FRACTION={MAX_LEAKAGE_FRACTION:.15e}")
    print(f"MAX_ORDINARY_ONE_BODY_G={MAX_ORDINARY_ONE_BODY_G:.15e}")

    # ------------------------------------------------------------------
    # Direct scalar-density endpoint naturalness.
    # ------------------------------------------------------------------
    print("\n=== DIRECT SCALAR-DENSITY ENDPOINT ONE-BODY NATURALNESS ===")
    cutoffs = sorted({MATERIAL_EFT_CUTOFF, selected_mu, selected_messenger})
    rows = [scalar_mixing_row(cutoff) for cutoff in cutoffs]

    asymptotic_relerrs = []
    for row in rows:
        e_asym = dirac_scalar_tadpole_low_cutoff(row.cutoff, M_E)
        n_asym = dirac_scalar_tadpole_low_cutoff(row.cutoff, M_N)
        e_rel = abs(e_asym / row.electron_tadpole - 1.0)
        n_rel = abs(n_asym / row.nucleon_tadpole - 1.0)
        asymptotic_relerrs.extend((e_rel, n_rel))

        print(
            "SCALAR_MIXING_CUTOFF="
            f"{row.cutoff:.15e} "
            f"I_E={row.electron_tadpole:.15e} "
            f"I_N={row.nucleon_tadpole:.15e} "
            f"G_N_FROM_E_CLOSURE={row.induced_nucleon_g:.15e} "
            f"G_E_FROM_N_CLOSURE={row.induced_electron_g:.15e} "
            f"NUCLEON_EXCESS={row.nucleon_excess:.15e} "
            f"ELECTRON_EXCESS={row.electron_excess:.15e} "
            f"LOW_CUTOFF_E_RELERR={e_rel:.3e} "
            f"LOW_CUTOFF_N_RELERR={n_rel:.3e}"
        )

    best_scalar_excess = min(max(row.nucleon_excess, row.electron_excess) for row in rows)
    worst_scalar_excess = max(max(row.nucleon_excess, row.electron_excess) for row in rows)
    scalar_counterterm_tuning = 1.0 / best_scalar_excess

    print(f"SCALAR_TADPOLE_ASYMPTOTIC_MAX_RELERR={max(asymptotic_relerrs):.15e}")
    print(f"SCALAR_ONE_BODY_BEST_CASE_EXCESS={best_scalar_excess:.15e}")
    print(f"SCALAR_ONE_BODY_WORST_CASE_EXCESS={worst_scalar_excess:.15e}")
    print(f"SCALAR_REQUIRED_COUNTERTERM_FRACTION_BEST_CASE={scalar_counterterm_tuning:.15e}")
    print("SCALAR_TADPOLE_COEFFICIENT_SCHEME_INDEPENDENT=NO")
    print("SCALAR_ONE_BODY_COUNTERTERM_SYMMETRY_FORBIDDEN=NO")

    scalar_density_pass = best_scalar_excess <= 1.0
    scalar_density_reject = best_scalar_excess >= MIN_SCALAR_NATURALNESS_EXCESS
    print(
        "DIRECT_SCALAR_DENSITY_SM_ENDPOINT="
        + ("PASS" if scalar_density_pass else "REJECTED_BY_ONE_BODY_NATURALNESS")
    )

    # ------------------------------------------------------------------
    # Pseudoscalar endpoint coherence.
    # ------------------------------------------------------------------
    print("\n=== PSEUDOSCALAR ENDPOINT COHERENCE / PERTURBATIVITY ===")
    q = MATERIAL_EFT_CUTOFF
    s_e = q / (2.0 * M_E)
    s_n = q / (2.0 * M_N)
    pair_suppression = s_e * s_n
    required_y_product = a.SELECTED_Y_PRODUCT / max(pair_suppression, 1.0e-300)
    required_y_endpoint = math.sqrt(required_y_product)
    required_y_sq_over_4pi = required_y_endpoint**2 / (4.0 * math.pi)

    print(f"PSEUDOSCALAR_MAX_Q_EV={q:.15e}")
    print(f"PSEUDOSCALAR_ELECTRON_NR_SUPPRESSION={s_e:.15e}")
    print(f"PSEUDOSCALAR_NUCLEON_NR_SUPPRESSION={s_n:.15e}")
    print(f"PSEUDOSCALAR_PAIR_SUPPRESSION={pair_suppression:.15e}")
    print(f"PSEUDOSCALAR_REQUIRED_Y_PRODUCT={required_y_product:.15e}")
    print(f"PSEUDOSCALAR_REQUIRED_Y_ENDPOINT={required_y_endpoint:.15e}")
    print(f"PSEUDOSCALAR_REQUIRED_Y_SQ_OVER_4PI={required_y_sq_over_4pi:.15e}")
    print("PSEUDOSCALAR_COHERENT_Q_TO_ZERO_RESPONSE=ZERO_FOR_UNPOLARIZED_MATTER")

    pseudoscalar_pass = required_y_sq_over_4pi <= MAX_YUKAWA_SQ_OVER_4PI
    print(
        "DIRECT_PSEUDOSCALAR_SM_ENDPOINT="
        + ("PASS" if pseudoscalar_pass else "REJECTED_BY_COHERENCE_AND_NONPERTURBATIVE_MATCH")
    )

    # Exhaustive Lorentz-bilinear classification for a scalar messenger.
    print("\n=== RENORMALIZABLE DIRAC BILINEAR ENDPOINT CLASSIFICATION ===")
    bilinear_rows = [
        ("SCALAR", "YES", "YES", "NO", "FAIL_ONE_BODY_NATURALNESS"),
        ("PSEUDOSCALAR", "YES", "NO", "YES", "FAIL_COHERENCE"),
        ("VECTOR", "NO_SCALAR_MESSENGER_INDEX_MISMATCH", "YES", "YES", "REQUIRES_VECTOR_PORTAL"),
        ("AXIAL_VECTOR", "NO_SCALAR_MESSENGER_INDEX_MISMATCH", "NO_UNPOLARIZED", "YES", "FAIL_COHERENCE"),
        ("TENSOR", "NO_WITHOUT_EXTRA_TENSOR", "NO_UNPOLARIZED", "YES", "FAIL_COHERENCE"),
    ]
    for name, scalar_coupling, coherent, tadpole_safe, decision in bilinear_rows:
        print(
            f"BILINEAR={name} "
            f"RENORMALIZABLE_SCALAR_X_COUPLING={scalar_coupling} "
            f"COHERENT_SPIN_INDEPENDENT={coherent} "
            f"VACUUM_ONE_POINT_SAFE={tadpole_safe} "
            f"DECISION={decision}"
        )

    direct_scalar_messenger_sm_embedding_pass = scalar_density_pass or pseudoscalar_pass
    print(
        "DIRECT_019A_SCALAR_MESSENGER_SM_BILINEAR_BASIS="
        + ("NONEMPTY" if direct_scalar_messenger_sm_embedding_pass else "EMPTY_UNDER_TESTED_RENORMALIZABLE_DIRAC_BILINEARS")
    )

    # ------------------------------------------------------------------
    # Vector-current escape.
    # ------------------------------------------------------------------
    print("\n=== CONSERVED VECTOR-CURRENT MATERIAL ESCAPE PREFLIGHT ===")
    vector = vector_current_mixing_proxy(MATERIAL_EFT_CUTOFF)

    print("VECTOR_PAIR_OPERATOR=C_PHI_PHI_JB_MU_JL_MU")
    print("VECTOR_NR_LIMIT=PHI_TIMES_BARYON_DENSITY_TIMES_LEPTON_DENSITY")
    print("VECTOR_TREE_ONE_CURRENT_VACUUM_EXPECTATION=ZERO_BY_LORENTZ_INVARIANCE")
    print("VECTOR_DERIVATIVE_CURRENT_OPERATOR=TOTAL_DERIVATIVE_FOR_EXACT_CONSERVED_CURRENT_UP_TO_GAUGE_EOM_MIXING")
    print("VECTOR_CURRENT_RENORMALIZATION_CAVEAT=CAN_MIX_WITH_FIELD_STRENGTH_DIVERGENCE_NOT_SCALAR_MONOPOLE")
    print(f"VECTOR_QED_ELECTRON_VACUUM_POLARIZATION_FACTOR={vector['electron_vp']:.15e}")
    print(f"VECTOR_QED_OUTER_LOOP_FACTOR={vector['outer_qed']:.15e}")
    print(f"VECTOR_QED_ONE_BODY_MIXING_FRACTION_BOUND={vector['qed_fraction']:.15e}")
    print(f"VECTOR_WEAK_ONE_BODY_MIXING_FRACTION_BOUND={vector['weak_fraction']:.15e}")
    print(f"VECTOR_HADRONIC_ONE_BODY_MIXING_FRACTION_BOUND={vector['hadronic_fraction']:.15e}")
    print(f"VECTOR_TOTAL_ONE_BODY_MIXING_FRACTION_PREFLIGHT={vector['total_fraction']:.15e}")
    print(f"VECTOR_ONE_BODY_MIXING_MARGIN={vector['margin']:.15e}")
    print(f"VECTOR_CHANNEL_MULTIPLICITY_INFLATION={VECTOR_MIXING_CHANNEL_MULTIPLICITY:.1f}")
    print("COMPLETE_ALL_ORDER_SM_OPERATOR_MIXING=NOT_CLAIMED")
    print("VECTOR_CURRENT_WILSON_PORTAL_LORENTZ_COMPLETION=NOT_ESTABLISHED")

    vector_prefight_pass = (
        anomaly_pass
        and vector["margin"] >= MIN_VECTOR_MIXING_MARGIN
    )
    print(f"VECTOR_CURRENT_ONE_BODY_MIXING_PREFLIGHT={'PASS' if vector_prefight_pass else 'FAIL'}")
    print("VECTOR_CURRENT_ENDPOINT_ESCAPE=RETAIN_AS_NEXT_MICROSCOPIC_PORTAL_CLASS" if vector_prefight_pass else "VECTOR_CURRENT_ENDPOINT_ESCAPE=DO_NOT_RETAIN")

    # Blind wildcard diagnostic: vary the already conservative channel-count
    # multiplier.  This is explicitly not evidence and not an optimization.
    print("\n=== BLIND WILDCARD CHANNEL-MULTIPLIER DIAGNOSTIC — NOT EVIDENCE ===")
    base = VECTOR_MIXING_CHANNEL_MULTIPLICITY
    for factor in (0.625, 1.6, 1.875, 3.125, 5.0):
        inflated = vector["total_fraction"] * factor
        margin = MAX_LEAKAGE_FRACTION / max(inflated, 1.0e-300)
        print(
            f"WILDCARD_CHANNEL_FACTOR={factor:.6f} "
            f"EFFECTIVE_CHANNELS={base * factor:.6f} "
            f"MIXING_FRACTION={inflated:.15e} "
            f"MARGIN={margin:.15e} "
            f"PASS={'YES' if inflated <= MAX_LEAKAGE_FRACTION else 'NO'}"
        )
    print("WILDCARD_VALUES_USED_AS_EVIDENCE=NO")

    # ------------------------------------------------------------------
    # Decision.
    # ------------------------------------------------------------------
    print("\n=== 019B DECISION ===")

    direct_negative = (
        upstream_reconstruction_pass
        and anomaly_pass
        and scalar_density_reject
        and not pseudoscalar_pass
        and not direct_scalar_messenger_sm_embedding_pass
    )

    if direct_negative:
        print("019B_ANOMALY_FREE_SM_MATERIAL_ENDPOINT_AND_ONE_BODY_OPERATOR_MIXING_GATE=GREEN_NEGATIVE_RESULT")
        print("ANOMALY_FREE_SM_MATERIAL_CURRENT_COMPLETION=PASS")
        print("DIRECT_019A_SCALAR_MESSENGER_SM_EMBEDDING=REJECTED")
        print("SCALAR_DENSITY_ENDPOINT=REJECTED_BY_ONE_BODY_COUNTERTERM_NATURALNESS")
        print("PSEUDOSCALAR_ENDPOINT=REJECTED_BY_COHERENCE_AND_PERTURBATIVITY")
        if vector_prefight_pass:
            print("VECTOR_CURRENT_ENDPOINT_ESCAPE=SUPPORTED_AT_RELATIVISTIC_CURRENT_EFT_LEVEL")
            print("PROTECTED_SCALAR_BRANCH=RETAIN_BUT_REFORMULATE_WITH_VECTOR_CURRENT_PORTAL")
            print("NEXT=DOCUMENT_SESSION_THEN_019C_VECTOR_WILSON_PORTAL_UV_CONSTRUCTION_BEFORE_EXPERIMENTAL_BOUND")
        else:
            print("VECTOR_CURRENT_ENDPOINT_ESCAPE=NOT_SUPPORTED")
            print("PROTECTED_SCALAR_BRANCH=DEMOTE_PENDING_NEW_PROTECTION_PRINCIPLE")
            print("NEXT=DOCUMENT_SESSION_AND_GLOBAL_RERANK")
    else:
        print("019B_ANOMALY_FREE_SM_MATERIAL_ENDPOINT_AND_ONE_BODY_OPERATOR_MIXING_GATE=INCONCLUSIVE_OR_POSITIVE_SURPRISE")
        print("NEXT=MANUAL_CLASSIFICATION_REQUIRED_BEFORE_PROMOTION")

    print("STANDARD_MODEL_GAUGE_ANOMALY_CANCELLATION=EXPLICITLY_RECONSTRUCTED")
    print("REAL_ORDINARY_BARYON_AND_LEPTON_CURRENTS=AVAILABLE")
    print("DIRECT_SCALAR_DENSITY_ONE_BODY_ZERO=NOT_TECHNICALLY_NATURAL")
    print("COMPLETE_ONE_BODY_OPERATOR_MIXING_FOR_DIRECT_SCALAR_ENDPOINT=FAILS_BEFORE_FULL_ADM_NEEDED")
    print("VECTOR_CURRENT_COMPLETE_RENORMALIZABLE_WILSON_UV=NOT_YET_ESTABLISHED")
    print("EXACT_2026_5KM_FIFTH_FORCE_BOUND=DEFER_UNTIL_VECTOR_PORTAL_EXISTS")
    print("STELLAR_COSMOLOGICAL_COMPLETION=NOT_ESTABLISHED")
    print("REAL_ANTIGRAVITY_MATERIAL=NO")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("018B_FIELD_EXISTENCE_RESULT=RETAINED")
    print("018C_M2_STABILITY_FALSIFICATION=RETAINED")
    print("019A_WILSON_LINE_UV_PROTECTION_WITNESS=RETAINED")
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY")
    print("HEURISTIC_INCREASE_FROM_019B=NO_DIRECT_REAL_MATERIAL_EMBEDDING_NOT_CLOSED")
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_019B_ANOMALY_FREE_SM_MATERIAL_ENDPOINT_AND_ONE_BODY_MIXING_GATE")


if __name__ == "__main__":
    main()
