"""R3X3B3 — conservative spin-dipole source-energy lower bound.

This preflight uses the corrected R3X1 finite-matter operator and the
R3X3B1 physically linked portal-scale parameter diagnostic.

For an external magnetic field generated only by pointlike spin
dipoles with effective moments mu_i and source-payload gap d:

    |B| <= (mu0 / 4pi) * (2 / d**3) * sum(|mu_i|).

If each source fermion has a magnetic moment no larger than mu_B
in the canonical field normalization, then its rest-energy floor
follows directly from the electron moment-to-rest-energy ratio.

This excludes only this declared dipole-source class.
It is NOT a hidden-sector no-go, complete-action validation, or
physical antigravity demonstration.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.constants import c, mu_0, physical_constants

from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    EV_J,
    HBAR_C_EV_M,
    TARGET_ACCELERATION_M_S2,
)
from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)
from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _fields_from_potentials,
    _vectors_to_full_potentials,
)
from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded,
    _state,
)


BRANCH = "032H17A12D1R3X3B3"
ENERGY_LIMIT_J = 10_000_000.0
STANDOFF_M = 1.0

ELECTRON_MASS_KG = physical_constants["electron mass"][0]
BOHR_MAGNETON_A_M2 = physical_constants["Bohr magneton"][0]

ELECTRON_MOMENT_PER_REST_J = (
    BOHR_MAGNETON_A_M2
    / (ELECTRON_MASS_KG * c**2)
)

# B is a canonical-Maxwell SI magnetic-energy equivalent.
B_SI_EQUIVALENT_FACTOR = math.sqrt(
    mu_0 * EV_J / HBAR_C_EV_M
)


def dipole_source_bound(b_t: float, gap_m: float = STANDOFF_M):
    """Return lower bounds for electron-moment dipole sources."""
    if not math.isfinite(b_t) or b_t < 0:
        raise ValueError("Magnetic field must be finite and nonnegative")

    if not math.isfinite(gap_m) or gap_m <= 0:
        raise ValueError("Source-to-payload gap must be positive")

    moment_min = (
        b_t * gap_m**3
        / (2.0 * mu_0 / (4.0 * math.pi))
    )

    rest_energy_min = (
        moment_min / ELECTRON_MOMENT_PER_REST_J
    )

    return {
        "b_payload_min_si_equivalent_t": b_t,
        "source_payload_gap_m": gap_m,
        "required_total_dipole_moment_a_m2": moment_min,
        "electron_sized_dipole_rest_energy_floor_j":
            rest_energy_min,
        "required_moment_per_mass_energy_enhancement":
            rest_energy_min / ENERGY_LIMIT_J,
        "electron_sized_dipole_source_passes_10mj":
            rest_energy_min < ENERGY_LIMIT_J,
        "other_microscopic_source_families_excluded": False,
    }


def evaluate_grid(h: float, loading: float = 5e-6):
    setup = _build_baseline_and_prep(h)

    solution = _solve_loaded(
        setup["prep"],
        loading,
        1.0,
    )

    if not solution.get("success"):
        raise RuntimeError("Corrected loaded solver failed")

    state = _state(setup, solution)

    a_min = float(
        state["minimum_payload_acceleration_m_s2"]
    )

    if a_min <= 0:
        return {
            "h_m": h,
            "outward_everywhere_sampled": False,
        }

    # Consistent R3X3B1 source and portal-scale adjustment.
    amplitude = math.sqrt(
        (TARGET_ACCELERATION_M_S2 / a_min) / loading
    )

    phi, a_phi = _vectors_to_full_potentials(
        setup["prep"],
        setup["field"],
        setup["phi0"],
        setup["a0"],
        solution,
    )

    fields = _fields_from_potentials(
        phi,
        a_phi,
        setup["field"]["rho_grid"],
        h,
    )

    b_code = np.hypot(
        fields["b_rho"],
        fields["b_z"],
    )

    b_payload = (
        b_code[setup["field"]["payload"]]
        * amplitude
        * B_SI_EQUIVALENT_FACTOR
    )

    bound = dipole_source_bound(
        float(np.min(b_payload))
    )

    return {
        "h_m": h,
        "relative_loading": loading,
        "portal_scale_keV": loading ** (-0.25),
        "outward_everywhere_sampled": True,
        "canonical_field_energy_for_1g_j":
            float(
                state["canonical_field_energy_j"]
                * amplitude**2
            ),
        "required_source_amplitude_multiplier": amplitude,
        "b_payload_max_si_equivalent_t":
            float(np.max(b_payload)),
        **bound,
    }


def run():
    grids = (0.075, 0.050, 0.040)

    records = []

    for h in grids:
        result = evaluate_grid(h)
        records.append(result)

        print(
            "GRID=", h,
            "B_MIN_T=",
            result.get("b_payload_min_si_equivalent_t"),
            "SOURCE_REST_FLOOR_J=",
            result.get(
                "electron_sized_dipole_rest_energy_floor_j"
            ),
            "REQUIRED_ENHANCEMENT=",
            result.get(
                "required_moment_per_mass_energy_enhancement"
            ),
            flush=True,
        )

    summary = {
        "branch": BRANCH,
        "source_scope":
            "ELECTRON_SIZED_STATIC_POLAR_MAGNETIC_DIPOLES",
        "model_scope":
            "CORRECTED_LORENTZIAN_FROZEN_DENSITY",
        "grids": records,
        "microscopic_hidden_source_excluded": False,
        "fully_loaded_nonlin_action_certified": False,
        "continuum_certified": False,
        "complete_energy_certified": False,
        "physical_antigravity_model_found": False,
        "r3b_preloaded_1p542916_j_preserved": True,
        "006d_replaced": False,
    }

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b3_dipole_source_energy_summary.json"
    )

    path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )

    print("R3X3B3_RESULT_PATH=", path)

    return summary


if __name__ == "__main__":
    run()
