r"""Simulation 015A — practical-path protected pair-portal decision gate.

PURPOSE
-------
Rerank the leading surviving speculative antigravity-like mechanisms after
the 014D local total-force reversal and 014E constant-disformal baryonic
bridge failure.

The calculation focuses on the current lowest-complexity practical candidate
from the earlier 010E material-state branch: a protected two-body scalar
response whose isolated constituents have no additional scalar charge.

SCIENTIFIC QUESTIONS
--------------------
1. Can an ordinary exact additive internal symmetry allow both a baseline
   relativistic pair/dimer mixing operator

       mu D^\dagger A B

   and a scalar-modulated mixing operator

       y phi D^\dagger A B

   while forbidding one-body scalar operators such as

       phi A^\dagger A

   and

       phi B^\dagger B?

2. Does the corresponding minimal scalar-field prototype possess a one-loop
   topology that radiatively generates the forbidden one-body operator?

3. How does the remaining UV burden of the 010E protected-composite route
   compare with the physical scale required by the 014D/014E disformal route?

4. Which branch currently has the highest information value for the next
   research slice aimed specifically at practical antigravity?

THEORY / MODEL
--------------
The protected-pair UV prototype contains fields A, B, and D with an additive
conserved internal charge satisfying

    q_D = q_A + q_B.

A baseline mixing interaction is

    mu D^\dagger A B + h.c.

and the minimal off-diagonal scalar portal is

    y phi D^\dagger A B + h.c.

For any additive exact symmetry, invariance of the first interaction requires

    -q_D + q_A + q_B = 0.

Invariance of the scalar-modulated interaction requires

    q_phi - q_D + q_A + q_B = 0.

Subtracting the two equations gives

    q_phi = 0.

Therefore the one-body density operators

    phi A^\dagger A
    phi B^\dagger B

are also invariant under that same additive symmetry.

The calculation independently verifies this statement by exhaustive Z_N
enumeration.

RADIATIVE PREFLIGHT
-------------------
With one baseline mixing vertex and one scalar-modulated mixing vertex,
external A legs can be connected through internal B and D propagators.

For a scalar prototype:

    L = 1 loop
    I = 2 internal propagators

and the superficial ultraviolet degree is

    omega = 4 L - 2 I = 0.

The graph is therefore logarithmically divergent by power counting and
requires a local phi A^\dagger A counterterm unless some additional
cancellation or structural protection exists.

The same argument applies with A and B exchanged.

This is a model-class preflight, not a universal theorem covering every
possible relativistic field content.

DISFORMAL SCALE COMPARISON
--------------------------
The 014E normalization is

    b0 = H0^2 M_Pl^2 / M_D^4

or

    M_D = sqrt(H0 M_Pl) b0^(-1/4).

The constants used here are copied from the independently recorded 014E
result so this script does not silently change cosmological conventions.

The first 014D local reversal occurs at b0 = 0.24 and the principal validated
candidate uses b0 = 0.28.

The direct constant-B Standard-Model comparison remains the project's
declared 650 GeV benchmark. This script does not claim that it represents
every environment-dependent or UV-complete disformal theory.

010E COMPARISON
---------------
The 010E low-energy protected-composite benchmarks used here are project
reference values only. In particular:

    mediator mass:
        3.946539608e-11 eV

    pair Wilson coefficient at the atomic EFT cutoff:
        2.713818830692468e-11

    atomic EFT cutoff:
        657.7566013333334 eV

    maximum target-equivalent ordinary-matter leakage:
        5.772961445324848e-7

The low-energy EFT surviving these checks does not imply that a relativistic
completion exists.

NUMERICAL METHOD
----------------
The script performs:

1. exact algebraic consistency checks;
2. exhaustive finite-group charge enumeration for Z_N, 2 <= N <= 64;
3. independent UV power counting;
4. physical-scale reconstruction of the 014E disformal suppression scale;
5. thermal-scale comparisons;
6. a conservative branch reranking based only on already established project
   obstacles.

The finite-group enumeration is distributed across available CPU processes.

VALIDATION
----------
The 014B-014E preserved source SHA-256 hashes are checked before conclusions
are printed.

The computed b0-to-M_D values are compared with the recorded 014E reference
values.

LIMITATIONS
-----------
This calculation does not establish:

- a universal no-go theorem for all UV completions;
- the absence of non-Abelian, derivative, topological, supersymmetric,
  nonperturbative, or emergent protection mechanisms;
- global-body lift in the 014D model;
- a real material with the 010E scalar portal;
- experimental antigravity;
- a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_ANALYTICAL_AND_COMPUTATIONAL_UV_PREFLIGHT

PRACTICAL ANTIGRAVITY DEVICE
----------------------------
NOT ESTABLISHED
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import math
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_HASHES = {
    "014b_disformal_repulsion_prerequisite.py":
        "8f6a3b0e5cb28546c456766d506460029b5f694a95ee76c526e0d842f945fb1b",
    "014c_decisive_disformal_force.py":
        "59132b42245d10187d1c26ff4ab75fa8c9cb36973bfc06420480013227dc93e1",
    "014d_disformal_total_reversal.py":
        "01220601e0ed71e84c79c94b36fec7d60b596572bc192b1ce168dec2db35d71c",
    "014e_baryonic_disformal_bridge.py":
        "b363cfadff64f73db80bc5e8f5ab65cddd95842431c6a610a9338d6f218956e6",
}

SQRT_H0_MPL_EV = 1.8757704502758766e-3

B0_FIRST_REVERSAL = 0.24
B0_VALIDATED = 0.28

REFERENCE_MD_FIRST_EV = 2.6799511607263058e-3
REFERENCE_MD_VALIDATED_EV = 2.5786368350373110e-3

COLLIDER_MD_EV = 650.0e9

KB_EV_K = 8.617333262e-5
PLANCK_EV_S = 4.135667696e-15

SCALAR_010E_MASS_EV = 3.946539608e-11
ATOMIC_EFT_CUTOFF_EV = 657.7566013333334
PAIR_WILSON_010E = 2.713818830692468e-11
ONE_BODY_LEAKAGE_ALLOWANCE = 5.772961445324848e-7
TARGET_DINUCLEAR_COUPLING = 8.638353631211470e-12
CONTROL_FREE_ENERGY_1000KG_J = 1.063556252028522e8

PROJECT_014E_HIERARCHY = 3.4605562139399018e57
PROJECT_014E_DELTA_LN_B = 132.48877963228443


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def disformal_md_ev(b0: float) -> float:
    return SQRT_H0_MPL_EV * b0 ** (-0.25)


def collider_safe_b0() -> float:
    return (SQRT_H0_MPL_EV / COLLIDER_MD_EV) ** 4


def enumerate_zn_case(n: int) -> tuple[int, int, int]:
    """Exhaustively check the minimal additive-charge portal under Z_N.

    q_D is fixed by the requirement that D^dagger A B be invariant.

    We then enumerate q_A, q_B, and q_phi and ask whether both the baseline
    and phi-modulated pair vertices can be invariant while phi A^dagger A
    and phi B^dagger B are forbidden.

    Returns
    -------
    tuple
        n,
        number of assignments allowing both pair vertices,
        number of assignments that additionally forbid both one-body terms.
    """
    both_pair_vertices = 0
    protected_survivors = 0

    for q_a in range(n):
        for q_b in range(n):
            q_d = (q_a + q_b) % n

            for q_phi in range(n):
                baseline = (-q_d + q_a + q_b) % n == 0
                modulated = (
                    q_phi - q_d + q_a + q_b
                ) % n == 0

                one_body_a = (
                    q_phi - q_a + q_a
                ) % n == 0

                one_body_b = (
                    q_phi - q_b + q_b
                ) % n == 0

                if baseline and modulated:
                    both_pair_vertices += 1

                    if not one_body_a and not one_body_b:
                        protected_survivors += 1

    return n, both_pair_vertices, protected_survivors


def main() -> None:
    print(
        "=== 015A — PRACTICAL PATH / PROTECTED PAIR-PORTAL "
        "DECISION GATE ==="
    )

    print()
    print("=== PRESERVED 014 SOURCE INTEGRITY ===")

    all_hashes_match = True

    for filename, expected in EXPECTED_HASHES.items():
        path = ROOT / "simulations" / filename

        if not path.exists():
            print(f"{filename}=MISSING")
            all_hashes_match = False
            continue

        actual = sha256_file(path)
        match = actual == expected

        print(f"{filename}_SHA256={actual}")
        print(f"{filename}_HASH_MATCH={match}")

        all_hashes_match &= match

    print(f"ALL_014_HASHES_MATCH={all_hashes_match}")

    print()
    print("=== 014E PHYSICAL SCALE RECONSTRUCTION ===")

    md_first = disformal_md_ev(B0_FIRST_REVERSAL)
    md_validated = disformal_md_ev(B0_VALIDATED)

    print(f"MD_B0_0P24_EV={md_first:.16e}")
    print(f"MD_B0_0P28_EV={md_validated:.16e}")

    first_rel_error = abs(
        md_first - REFERENCE_MD_FIRST_EV
    ) / REFERENCE_MD_FIRST_EV

    validated_rel_error = abs(
        md_validated - REFERENCE_MD_VALIDATED_EV
    ) / REFERENCE_MD_VALIDATED_EV

    print(
        "MD_B0_0P24_REFERENCE_REL_ERROR="
        f"{first_rel_error:.16e}"
    )

    print(
        "MD_B0_0P28_REFERENCE_REL_ERROR="
        f"{validated_rel_error:.16e}"
    )

    safe_b0 = collider_safe_b0()
    hierarchy = B0_FIRST_REVERSAL / safe_b0
    delta_ln_b = math.log(hierarchy)

    print(f"COLLIDER_SAFE_B0={safe_b0:.16e}")
    print(f"INDEPENDENT_B_HIERARCHY={hierarchy:.16e}")
    print(f"INDEPENDENT_DELTA_LN_B={delta_ln_b:.16e}")

    hierarchy_rel_error = abs(
        hierarchy - PROJECT_014E_HIERARCHY
    ) / PROJECT_014E_HIERARCHY

    print(
        "PROJECT_014E_HIERARCHY_REL_ERROR="
        f"{hierarchy_rel_error:.16e}"
    )

    print()
    print("=== DISFORMAL THERMAL / EFT SCALE CHECK ===")

    cutoff_temperature_first_k = md_first / KB_EV_K
    cutoff_temperature_validated_k = md_validated / KB_EV_K

    print(
        "B0_0P24_MD_EQUIVALENT_TEMPERATURE_K="
        f"{cutoff_temperature_first_k:.12f}"
    )

    print(
        "B0_0P28_MD_EQUIVALENT_TEMPERATURE_K="
        f"{cutoff_temperature_validated_k:.12f}"
    )

    for temperature_k in (4.0, 28.13102372293623, 77.0, 300.0):
        thermal_ev = KB_EV_K * temperature_k

        print(
            f"T_{temperature_k:.6f}K_KBT_EV="
            f"{thermal_ev:.16e}"
        )

        print(
            f"T_{temperature_k:.6f}K_KBT_OVER_MD_0P24="
            f"{thermal_ev / md_first:.16e}"
        )

        print(
            f"T_{temperature_k:.6f}K_KBT_OVER_MD_0P28="
            f"{thermal_ev / md_validated:.16e}"
        )

    controlled_0p1_first_k = 0.1 * md_first / KB_EV_K
    controlled_0p1_validated_k = 0.1 * md_validated / KB_EV_K

    print(
        "T_FOR_KBT_OVER_MD_0P1_B0_0P24_K="
        f"{controlled_0p1_first_k:.12f}"
    )

    print(
        "T_FOR_KBT_OVER_MD_0P1_B0_0P28_K="
        f"{controlled_0p1_validated_k:.12f}"
    )

    cutoff_frequency_hz = md_first / PLANCK_EV_S

    print(
        "B0_0P24_MD_FREQUENCY_HZ="
        f"{cutoff_frequency_hz:.16e}"
    )

    print()
    print("=== 010E LOW-ENERGY EFT SCALE CHECK ===")

    kbt_77_ev = KB_EV_K * 77.0

    print(
        "010E_ATOMIC_EFT_CUTOFF_EV="
        f"{ATOMIC_EFT_CUTOFF_EV:.16e}"
    )

    print(
        "010E_77K_KBT_OVER_ATOMIC_EFT_CUTOFF="
        f"{kbt_77_ev / ATOMIC_EFT_CUTOFF_EV:.16e}"
    )

    print(
        "010E_PAIR_WILSON="
        f"{PAIR_WILSON_010E:.16e}"
    )

    print(
        "010E_TARGET_DINUCLEAR_COUPLING="
        f"{TARGET_DINUCLEAR_COUPLING:.16e}"
    )

    print(
        "010E_1000KG_CONTROL_FREE_ENERGY_SCALE_J="
        f"{CONTROL_FREE_ENERGY_1000KG_J:.16e}"
    )

    generic_loop = 1.0 / (16.0 * math.pi**2)
    loop_to_allowance = generic_loop / ONE_BODY_LEAKAGE_ALLOWANCE

    print(
        "GENERIC_ONE_LOOP_FACTOR="
        f"{generic_loop:.16e}"
    )

    print(
        "010E_ONE_BODY_LEAKAGE_ALLOWANCE="
        f"{ONE_BODY_LEAKAGE_ALLOWANCE:.16e}"
    )

    print(
        "GENERIC_LOOP_TO_LEAKAGE_ALLOWANCE_RATIO="
        f"{loop_to_allowance:.16e}"
    )

    print()
    print("=== EXACT ADDITIVE-SYMMETRY ARGUMENT ===")

    print(
        "BASELINE_VERTEX_CHARGE="
        "-q_D+q_A+q_B"
    )

    print(
        "SCALAR_VERTEX_CHARGE="
        "q_phi-q_D+q_A+q_B"
    )

    print(
        "SUBTRACTING_INVARIANCE_CONDITIONS_GIVES="
        "q_phi=0"
    )

    print(
        "ONE_BODY_OPERATOR_CHARGE="
        "q_phi"
    )

    print(
        "ANALYTIC_SIMPLE_ADDITIVE_SYMMETRY_PROTECTION="
        "IMPOSSIBLE_IN_THIS_MINIMAL_PORTAL"
    )

    print()
    print("=== INDEPENDENT Z_N EXHAUSTIVE ENUMERATION ===")

    max_n = 64
    requested_workers = int(
        os.environ.get(
            "AG_RESEARCH_NCPU",
            str(os.cpu_count() or 1),
        )
    )

    workers = max(
        1,
        min(
            requested_workers,
            max_n - 1,
        ),
    )

    print(f"ZN_MAX_N={max_n}")
    print(f"ZN_WORKERS={workers}")

    with concurrent.futures.ProcessPoolExecutor(
        max_workers=workers
    ) as executor:
        results = list(
            executor.map(
                enumerate_zn_case,
                range(2, max_n + 1),
            )
        )

    total_pair_allowed = sum(
        item[1]
        for item in results
    )

    total_protected = sum(
        item[2]
        for item in results
    )

    print(
        "ZN_TOTAL_ASSIGNMENTS_WITH_BOTH_PAIR_VERTICES="
        f"{total_pair_allowed}"
    )

    print(
        "ZN_PROTECTED_ASSIGNMENTS_FOUND="
        f"{total_protected}"
    )

    print(
        "ZN_ENUMERATION_CONFIRMS_ANALYTIC_NO_GO="
        f"{total_protected == 0}"
    )

    for n, pair_allowed, protected in results[:8]:
        print(
            f"ZN_N={n} "
            f"PAIR_ALLOWED={pair_allowed} "
            f"PROTECTED={protected}"
        )

    print()
    print("=== ONE-LOOP COUNTERTERM POWER COUNTING ===")

    loops = 1
    internal_scalar_lines = 2

    superficial_degree = (
        4 * loops
        - 2 * internal_scalar_lines
    )

    print(f"LOOPS={loops}")
    print(f"INTERNAL_SCALAR_LINES={internal_scalar_lines}")
    print(
        "SUPERFICIAL_UV_DEGREE="
        f"{superficial_degree}"
    )

    print(
        "ONE_BODY_LOOP_DIVERGENCE="
        + (
            "LOGARITHMIC"
            if superficial_degree == 0
            else "OTHER"
        )
    )

    print(
        "PHI_A_DAGGER_A_COUNTERTERM_ALLOWED="
        "YES"
    )

    print(
        "PHI_B_DAGGER_B_COUNTERTERM_ALLOWED="
        "YES"
    )

    print(
        "MINIMAL_OFFDIAGONAL_DIMER_PORTAL_"
        "TECHNICALLY_NATURAL_ONE_BODY_ZERO="
        "NO_WITHOUT_ADDITIONAL_PROTECTION"
    )

    print()
    print("=== PRACTICAL-PATH RERANK ===")

    print(
        "006D_CLASSICAL_GR="
        "ESTABLISHED_LOCAL_REPULSION_BUT_"
        "CATASTROPHIC_AH2_OVER_G_SCALE"
    )

    print(
        "014D_DISFORMAL_LOCAL_REVERSAL="
        "POSITIVE_NUMERICAL_RESULT"
    )

    print(
        "014D_GLOBAL_BODY_LIFT="
        "NOT_ESTABLISHED"
    )

    print(
        "014E_DIRECT_CONSTANT_B_BARYONIC_BRIDGE="
        "REJECTED"
    )

    print(
        "010E_LOW_ENERGY_PROTECTED_COMPOSITE_EFT="
        "PARAMETRIC_SURVIVOR"
    )

    print(
        "010E_SIMPLE_ADDITIVE_SYMMETRY_UV_PROTECTION="
        "REJECTED_BY_015A_MINIMAL_PORTAL_GATE"
    )

    print(
        "COMMON_SURVIVING_ARCHITECTURE="
        "EMERGENT_OR_GENUINELY_PAIR_SPECIFIC_"
        "COLLECTIVE_SECTOR_WITH_STRUCTURAL_"
        "SEQUESTERING"
    )

    print(
        "PRACTICAL_ROUTE_PRIORITY_1="
        "PROTECTED_COLLECTIVE_SOURCE_REFERENCED_"
        "FIFTH_FORCE_WITH_NONTRIVIAL_UV_PROTECTION"
    )

    print(
        "PRACTICAL_ROUTE_PRIORITY_2="
        "014D_DISFORMAL_ONLY_IF_GLOBAL_BODY_FORCE_"
        "AND_NONUNIVERSAL_UV_BRIDGE_BOTH_SURVIVE"
    )

    print(
        "PRACTICAL_ROUTE_PRIORITY_3="
        "006D_CLASSICAL_GR_ONLY_IF_NEW_MATTER_"
        "MECHANISM_CHANGES_PARAMETRIC_SCALING"
    )

    print()
    print("=== 015A DECISION ===")

    if not all_hashes_match:
        print(
            "015A_GATE=INVALID_014_SOURCE_INTEGRITY_FAILURE"
        )
        return

    if total_protected != 0:
        print(
            "015A_GATE=UNEXPECTED_SYMMETRY_SURVIVOR_REVIEW_REQUIRED"
        )
        return

    print(
        "MINIMAL_RELATIVISTIC_PAIR_PORTAL="
        "REJECTED_AS_SUFFICIENT_PROTECTION"
    )

    print(
        "ORDINARY_ADDITIVE_PARTICLE_NUMBER_"
        "PROTECTION_ALONE="
        "INSUFFICIENT"
    )

    print(
        "NEXT_REQUIRED_PROTECTION_CLASS="
        "NONTRIVIAL_PAIR_REPRESENTATION_OR_"
        "EMERGENT_SEQUESTERING_OR_"
        "CANCELLATION_STRUCTURE"
    )

    print(
        "NEXT_HIGHEST_INFORMATION_GATE="
        "015B_EXPLICIT_PAIR_SPECIFIC_UV_"
        "OPERATOR_BASIS_AND_ONE_BODY_MIXING"
    )

    print(
        "PARALLEL_DISFORMAL_STOP_GATE="
        "FINITE_SOURCE_FINITE_PAYLOAD_GLOBAL_FORCE"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_MINIMAL_RELATIVISTIC_"
        "PAIR_PORTAL_UV_PREFLIGHT"
    )


if __name__ == "__main__":
    main()
