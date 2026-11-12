"""032H17A12D1R3X3B16 — finite-mass weak-loading crossover audit.

Scientific target
-----------------
Map the corrected Lorentzian R3B static loaded response into
physical payload mass.

Preserve the original source, torus geometry, 1 m clearance,
1-keV portal, and canonical field normalization.

In this frozen-beta model:

    beta = -constant * matter_density

Replacing density by f*density is exactly equivalent to
solving the existing full-density coupled operator with
homotopy parameter lambda=f.

Therefore this does not claim a new mechanism beyond B0.

Additional observables:
- Actual integrated neutral-payload mass.
- Loaded density-weighted COM acceleration.
- Positive and negative total force contributions.
- Negative-mass fraction and worst-point location.
- Loaded field deviation and canonical field energy.
- Grid-dependent strict-1g and outward-sign thresholds.
- Independent scaled-density/operator equivalence.

Important limitations
---------------------
A milligram-scale payload is distributed over the original
full-size, extremely dilute torus, not a compact solid object.

The zero-density control contains no payload and has zero force.

Neither microscopic sourcing, complete matter dynamics,
source reaction, stable propagation, whole-craft lift,
nor complete device energy is established.

006D is not replaced.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    PAYLOAD_MAJOR_RADIUS_M,
    PAYLOAD_MINOR_RADIUS_M,
    REFERENCE_PORTAL_SCALE_EV,
    SOURCE_RADIUS_M,
    payload_center_z_m,
)
from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)
from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded,
)
from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _fields_from_potentials,
    _prepare_low_rank_loaded_system,
    _vectors_to_full_potentials,
)
from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
    loading_coefficient_z,
)

BRANCH = "032H17A12D1R3X3B16"
TARGET = 9.80665

KAPPA = (
    -2.0
    * HBAR_C_EV_M**2
    / REFERENCE_PORTAL_SCALE_EV**4
)

FRACTIONS = (
    0.0,
    1e-8,
    1e-7,
    1e-6,
    3e-6,
    5e-6,
    8e-6,
    8.6e-6,
    1e-5,
    2e-5,
    3e-5,
    1e-4,
    1e-3,
    1e-2,
    0.1,
    1.0,
)


def physical_standoff_m():
    return (
        math.hypot(
            PAYLOAD_MAJOR_RADIUS_M,
            payload_center_z_m(),
        )
        - PAYLOAD_MINOR_RADIUS_M
        - SOURCE_RADIUS_M
    )


def finite_volume_force(density, acceleration, volume):
    weighted = density * acceleration * volume

    negative = acceleration < 0

    return {
        "net_n": float(np.sum(weighted)),
        "positive_n": float(
            np.sum(np.maximum(weighted, 0.0))
        ),
        "negative_n": float(
            np.sum(np.minimum(weighted, 0.0))
        ),
        "negative_mass_fraction": float(
            np.sum(density[negative] * volume[negative])
            / max(
                float(np.sum(density * volume)),
                1e-300,
            )
        ),
    }


class Response:
    """Reuse the original R3B background and one loaded operator."""

    def __init__(self, h):
        self.h = float(h)

        self.setup = _build_baseline_and_prep(self.h)
        self.field = self.setup["field"]
        self.rho = self.field["rho_grid"]
        self.density_ref = self.setup["density"]

        self.volume = (
            2.0 * np.pi * self.rho * self.h**2
        )

        self.active = (
            (self.density_ref > 0)
            & self.field["payload"]
        )

        self.ref_mass = float(
            np.sum(self.volume * self.density_ref)
        )

        self.peak_beta = float(
            np.max(np.abs(self.setup["beta_full"]))
        )

        self.reference_fields = _fields_from_potentials(
            self.setup["phi0"],
            self.setup["a0"],
            self.rho,
            self.h,
        )

        self.reference_energy = self.energy_j(
            self.reference_fields
        )

        self.reference_norm = max(
            self.field_norm(self.reference_fields),
            1e-300,
        )

        self._cache = {}

    def field_norm(self, fields):
        return float(np.sqrt(sum(
            np.sum(self.volume * fields[key]**2)
            for key in (
                "e_rho",
                "e_z",
                "b_rho",
                "b_z",
            )
        )))

    def energy_j(self, fields):
        return (
            0.5
            * self.field_norm(fields)**2
            / HBAR_C_EV_M
            * EV_J
        )

    def evaluate(self, f):
        f = float(f)

        if (
            not np.isfinite(f)
            or f < 0.0
            or f > 1.0
        ):
            raise ValueError(
                "Physical density fraction must lie in [0,1]"
            )

        if f in self._cache:
            return self._cache[f]

        solution = _solve_loaded(
            self.setup["prep"],
            f,
            1.0,
        )

        if not solution["success"]:
            raise RuntimeError(
                f"Loaded solve failed at f={f}"
            )

        if solution["relative_residual"] > 1e-8:
            raise RuntimeError(
                f"Loaded solver residual too large at f={f}"
            )

        phi, a = _vectors_to_full_potentials(
            self.setup["prep"],
            self.field,
            self.setup["phi0"],
            self.setup["a0"],
            solution,
        )

        fields = _fields_from_potentials(
            phi,
            a,
            self.rho,
            self.h,
        )

        sigma = KAPPA * (
            fields["e_rho"] * fields["b_rho"]
            + fields["e_z"] * fields["b_z"]
        )

        acceleration = (
            -C_LIGHT_M_S**2
            * np.gradient(
                sigma,
                self.h,
                axis=0,
                edge_order=2,
            )
        )

        density = f * self.density_ref
        mass = f * self.ref_mass

        force = finite_volume_force(
            density,
            acceleration,
            self.volume,
        )

        # At f=0, this is only the limiting response
        # weighted by the reference profile.
        com = float(
            np.sum(
                self.volume
                * self.density_ref
                * acceleration
            )
            / self.ref_mass
        )

        active_values = acceleration[self.active]

        worst_position = int(
            np.argmin(active_values)
        )

        j, i = map(
            int,
            np.argwhere(self.active)[worst_position],
        )

        deviation = math.sqrt(sum(
            np.sum(
                self.volume
                * (
                    fields[key]
                    - self.reference_fields[key]
                )**2
            )
            for key in (
                "e_rho",
                "e_z",
                "b_rho",
                "b_z",
            )
        )) / self.reference_norm

        minimum = float(
            np.min(active_values)
        )

        result = {
            "density_fraction": f,
            "actual_payload_mass_kg": mass,
            "massless_control": bool(f == 0.0),
            "peak_absolute_beta": self.peak_beta * f,
            "stand_off_m": physical_standoff_m(),

            "min_loaded_m_s2": minimum,
            "max_loaded_m_s2": float(
                np.max(active_values)
            ),

            "density_weighted_com_m_s2":
                com if f > 0 else None,

            "zero_mass_limiting_profile_mean_m_s2":
                com if f == 0 else None,

            "net_force_n": force["net_n"],
            "positive_force_n": force["positive_n"],
            "negative_force_n": force["negative_n"],

            "negative_mass_fraction":
                force["negative_mass_fraction"]
                if f > 0 else None,

            "negative_sample_count": int(
                np.count_nonzero(active_values < 0)
            ),

            "active_payload_cell_count": int(
                np.count_nonzero(self.active)
            ),

            "worst_rho_m": float(
                self.rho[j, i]
            ),

            "worst_z_m": float(
                self.field["z_grid"][j, i]
            ),

            "canonical_field_energy_j":
                self.energy_j(fields),

            "relative_field_change_from_preloaded":
                deviation,

            "condition_number":
                solution["condition_number"],

            "loaded_solver_relative_residual":
                solution["relative_residual"],

            "everywhere_outward": bool(
                f > 0 and minimum > 0
            ),

            "everywhere_ge_1g": bool(
                f > 0 and minimum >= TARGET
            ),

            "true_total_source_reaction_certified":
                False,
        }

        self._cache[f] = result

        return result

    def bracket_first_transition(
        self,
        key,
        threshold,
        fractions=FRACTIONS,
    ):
        """Bracket first sampled favorable-to-unfavorable crossing.

        This is a local numerical bracket, not a continuum
        threshold or a proof of global monotonicity.
        """
        probes = sorted(
            f for f in fractions if f > 0
        )

        prior_f = None

        for f in probes:
            y = self.evaluate(f)[key] - threshold

            if prior_f is not None and y < 0:
                low = prior_f
                hi = f

                if (
                    self.evaluate(low)[key]
                    < threshold
                ):
                    continue

                for _ in range(24):
                    mid = (low + hi) / 2.0

                    if (
                        self.evaluate(mid)[key]
                        >= threshold
                    ):
                        low = mid
                    else:
                        hi = mid

                return {
                    "last_passing_fraction": low,
                    "first_failing_fraction": hi,
                    "last_passing_mass_kg":
                        low * self.ref_mass,
                    "first_failing_mass_kg":
                        hi * self.ref_mass,
                    "local_only": True,
                }

            if y >= 0:
                prior_f = f

        return None

    def direct_scaled_operator_equivalence(
        self,
        f=1e-4,
    ):
        """Rebuild actual density-scaled beta independently."""

        z = loading_coefficient_z(
            f * self.density_ref,
            REFERENCE_PORTAL_SCALE_EV,
        )

        beta = -(z - 1.0)

        independently_prepared = (
            _prepare_low_rank_loaded_system(
                self.field,
                self.setup["phi0"],
                self.setup["a0"],
                beta,
            )
        )

        original = _solve_loaded(
            self.setup["prep"],
            f,
            1.0,
        )

        independent = _solve_loaded(
            independently_prepared,
            1.0,
            1.0,
        )

        if (
            not original["success"]
            or not independent["success"]
        ):
            raise RuntimeError(
                "One of the equivalence solves failed"
            )

        x = np.r_[
            original["delta_phi_vec"],
            original["delta_a_vec"],
        ]

        y = np.r_[
            independent["delta_phi_vec"],
            independent["delta_a_vec"],
        ]

        return {
            "density_fraction": f,

            "relative_solution_difference": float(
                np.linalg.norm(x - y)
                / max(
                    np.linalg.norm(x),
                    1e-300,
                )
            ),

            "relative_beta_difference": float(
                np.linalg.norm(
                    beta - f * self.setup["beta_full"]
                )
                / max(
                    np.linalg.norm(beta),
                    1e-300,
                )
            ),

            "independent_operator_residual":
                independent["relative_residual"],
        }


def run(
    h,
    fractions=FRACTIONS,
    certify_equivalence=True,
):
    scan = Response(h)

    rows = [
        scan.evaluate(f)
        for f in fractions
    ]

    equivalence = (
        scan.direct_scaled_operator_equivalence(1e-4)
        if certify_equivalence
        else None
    )

    return {
        "branch": BRANCH,
        "scope":
            "CORRECTED_LORENTZIAN_R3B_FROZEN_BETA_PHYSICAL_MASS_SCAN",

        "grid_m": float(h),

        "reference_mass_discrete_kg":
            scan.ref_mass,

        "stand_off_m":
            physical_standoff_m(),

        "source_preloaded_unchanged": True,

        "reference_preloaded_energy_j":
            scan.reference_energy,

        "reference_r3b_recorded_preloaded_energy_j":
            1.5429162116460216,

        "homotopy_equals_scaled_density_in_frozen_action":
            True,

        "prior_b0_1g_threshold_known":
            True,

        "direct_scaled_operator_equivalence":
            equivalence,

        "sampled_first_1g_loss":
            scan.bracket_first_transition(
                "min_loaded_m_s2",
                TARGET,
            ),

        "sampled_first_outward_sign_loss":
            scan.bracket_first_transition(
                "min_loaded_m_s2",
                0.0,
            ),

        "results": rows,

        "zero_density_is_no_payload": True,
        "full_nonlinear_matter_action_certified": False,
        "physical_microscopic_source_certified": False,
        "source_reaction_and_complete_energy_certified":
            False,
        "full_3d_tilted_source_solved": False,
        "physical_antigravity_established": False,
        "006d_replaced": False,
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--grids",
        nargs="+",
        type=float,
        default=(0.075, 0.05, 0.04),
    )

    parser.add_argument(
        "--skip-equivalence",
        action="store_true",
    )

    args = parser.parse_args()

    output = (
        Path(__file__).resolve().parents[1]
        / "results"
        / "data"
    )

    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    for h in args.grids:
        result = run(
            h,
            certify_equivalence=not args.skip_equivalence,
        )

        tag = f"{round(h * 1000):03d}"

        path = (
            output
            / f"032h17a12d1r3x3b16_weakload_h{tag}_summary.json"
        )

        path.write_text(
            json.dumps(
                result,
                indent=2,
                sort_keys=True,
            ) + "\n",
            encoding="utf-8",
        )

        print(
            f"B16 h={h:.3f} "
            f"ref_mass="
            f"{result['reference_mass_discrete_kg']:.8f}kg",
            flush=True,
        )

        print(
            "1G_GATE",
            result["sampled_first_1g_loss"],
            flush=True,
        )

        print(
            "SIGN_GATE",
            result["sampled_first_outward_sign_loss"],
            flush=True,
        )

        for row in result["results"]:
            print(
                f"f={row['density_fraction']:10.4g} "
                f"m={row['actual_payload_mass_kg']:.6g}kg "
                f"min={row['min_loaded_m_s2']:+10.5f} "
                f"COM={row['density_weighted_com_m_s2']} "
                f"F={row['net_force_n']:+.6e}N "
                f"negative_frac={row['negative_mass_fraction']}",
                flush=True,
            )

        print("FULL_PHYSICAL_MODEL=NO")
        print("RESULT=", path, flush=True)


if __name__ == "__main__":
    main()
