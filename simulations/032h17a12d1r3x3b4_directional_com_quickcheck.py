"""R3X3B4: directional COM and exact interface-force identity.

Corrected Lorentzian frozen-density R3B mirror.
No physical source, compensator, or spacecraft thrust is certified.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
    TARGET_ACCELERATION_M_S2,
)
from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)
from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded,
)
from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _vectors_to_full_potentials,
    _fields_from_potentials,
)

KAPPA = (
    -2.0
    * HBAR_C_EV_M**2
    / REFERENCE_PORTAL_SCALE_EV**4
)


def measure(setup, phi, a_phi):
    field = setup["field"]
    h = float(field["h"])

    volume = 2.0 * math.pi * field["rho_grid"] * h**2
    density = setup["density"]

    em = _fields_from_potentials(
        phi, a_phi, field["rho_grid"], h
    )

    p = (
        em["e_rho"] * em["b_rho"]
        + em["e_z"] * em["b_z"]
    )

    sigma = KAPPA * p

    acceleration = (
        -C_LIGHT_M_S**2
        * np.gradient(sigma, h, axis=0, edge_order=2)
    )

    density_gradient_z = np.gradient(
        density, h, axis=0, edge_order=2
    )

    mass = float(np.sum(volume * density))

    force_direct = float(
        np.sum(volume * density * acceleration)
    )

    force_interface = float(
        C_LIGHT_M_S**2
        * np.sum(volume * sigma * density_gradient_z)
    )

    assert mass > 0.0

    assert math.isclose(
        force_direct,
        force_interface,
        rel_tol=1e-10,
        abs_tol=1e-10,
    ), "Finite-payload force identity failed"

    return {
        "com_acceleration_m_s2": force_direct / mass,
        "minimum_payload_acceleration_m_s2": float(
            np.min(acceleration[field["payload"]])
        ),
        "positive_acceleration_mass_fraction": float(
            np.sum(
                volume * density * (acceleration > 0.0)
            ) / mass
        ),
        "force_identity_relative_error": (
            abs(force_direct - force_interface)
            / max(abs(force_direct), 1e-15)
        ),
    }


def run():
    records = []

    for h in (0.075, 0.050, 0.040):
        setup = _build_baseline_and_prep(h)

        preloaded = measure(
            setup, setup["phi0"], setup["a0"]
        )

        solution = _solve_loaded(
            setup["prep"], 1.0, 1.0
        )

        assert solution["success"]

        phi, a_phi = _vectors_to_full_potentials(
            setup["prep"],
            setup["field"],
            setup["phi0"],
            setup["a0"],
            solution,
        )

        loaded = measure(setup, phi, a_phi)

        assert (
            preloaded["minimum_payload_acceleration_m_s2"]
            >= TARGET_ACCELERATION_M_S2 - 1e-6
        )

        assert (
            loaded["com_acceleration_m_s2"]
            < TARGET_ACCELERATION_M_S2
        )

        records.append({
            "h_m": h,
            "preloaded": preloaded,
            "fully_loaded": loaded,
        })

        print(
            f"h={h:.3f} "
            f"preCOM={preloaded['com_acceleration_m_s2']:.8f} "
            f"loadedCOM={loaded['com_acceleration_m_s2']:.8f} "
            f"loadedMin="
            f"{loaded['minimum_payload_acceleration_m_s2']:.8f}",
            flush=True,
        )

    result = {
        "branch": "032H17A12D1R3X3B4",
        "original_benchmark_is_directional": True,
        "loaded_original_mirror_fails_com_1g": True,
        "exact_interface_force_identity_verified": True,
        "alternative_loaded_field_profiles_excluded": False,
        "new_compensator_certified": False,
        "continuum_certified": False,
        "complete_energy_certified": False,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
        "grids": records,
    }

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b4_directional_com_summary.json"
    )

    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )

    print("RESULT_PATH=", path)


if __name__ == "__main__":
    run()
