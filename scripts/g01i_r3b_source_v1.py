"""G01-I: R3B electrostatic mirror source/support obligations.

Reconstruct the original R3B shell charges and Maxwell tractions.
All results are necessary conditions, not a physical source solution.
Preserve the historical 1.5429162116460216 J capacity and loaded failure.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import secrets
import sys
import tarfile

import numpy as np
from numpy.polynomial.legendre import legval, legder, leggauss

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/gravity2/g01i_runs"

R3B_FILE = (
    "results/data/"
    "032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json"
)

PIN = {
    "src/antigravity_research/agminer/"
    "hook17_fdual_f_global_mirror_prefight.py":
        "aa8f196fcae6a63405181ca62674e22ac67e5da88303759bdd99d25716fa2263",
    "src/antigravity_research/agminer/"
    "hook17_f2_strong_payload_loading_rescue.py":
        "e1296794c25a4d0e4d5634c7e7d543a0b488b8d2a1963afcf7878bea1c1b99e7",
    "src/antigravity_research/delta1/"
    "delta1_02_r3b_portal_rank.py":
        "04d8d669adb1e4b067e75a285dd13f0fbaa6bbd879090b88e850a277baca9395",
    R3B_FILE:
        "9474b6782104abb5bd8dd5e893137621b30ad96109e3e52c5a01268794810b11",
}

REF = 1.5429162116460216
R = 2.0


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def encode(obj):
    return (
        json.dumps(obj, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode()


def sealed(path, data):
    if path.exists() or path.is_symlink():
        raise ValueError("IMMUTABLE_OUTPUT_EXISTS:" + path.name)

    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def parent():
    locks = {}

    for relative, expected in PIN.items():
        path = ROOT / relative

        if (
            not path.is_file()
            or path.is_symlink()
            or digest(path) != expected
        ):
            raise ValueError("R3B_PARENT_PIN_HOLD:" + relative)

        locks[relative] = expected

    document = json.loads((ROOT / R3B_FILE).read_text())

    if (
        document.get("branch") != "032H17A12D1R3B"
        or document.get("surface_charge_physicalized") is not False
        or document.get("full_loaded_topological_bvp_completed") is not False
    ):
        raise ValueError("ORIGINAL_R3B_CLAIM_DRIFT")

    fine = document["grid_results"]["0.05"]
    coarse = document["grid_results"]["0.075"]
    energy = fine["global_energy"]

    capacity = fine["payload_reconstruction"][
        "normalized_mixed_global_field_energy_j"
    ]

    if (
        abs(capacity - REF) > 1e-9
        or coarse["payload_reconstruction"][
            "normalized_mixed_global_field_energy_j"
        ] <= 0
    ):
        raise ValueError("R3B_PROTECTED_CAPACITY_DRIFT")

    normalization = float(capacity) / energy[
        "mixed_global_field_energy_before_1g_renormalization_j"
    ]

    if not math.isfinite(normalization) or normalization <= 0:
        raise ValueError("R3B_BAD_NORMALIZATION")

    original_modes = fine["multipole_modes"]

    if (
        not 1 <= len(original_modes) <= 32
        or [m["ell"] for m in original_modes]
        != list(range(1, len(original_modes) + 1))
    ):
        raise ValueError("R3B_BAD_MULTIPOLE_SET")

    modes = []
    conversion_factors = []

    for source in original_modes:
        ell = int(source["ell"])
        amplitude = float(source["boundary_scalar_amplitude"])
        magnetic = float(source["magnetic_exterior_energy_j"])

        if magnetic > 0 and abs(amplitude) > 1e-30:
            conversion_factors.append(
                magnetic / (
                    2 * math.pi * R
                    * (ell + 1) / (2 * ell + 1)
                    * amplitude**2
                )
            )

        modes.append({
            "ell": ell,
            "amplitude": amplitude,
            "magnetic_exterior_energy_j": magnetic,
            "electric_exterior_energy_j": float(
                source["electric_exterior_energy_j"]
            ),
            "electric_interior_energy_j": float(
                source["electric_interior_energy_j"]
            ),
            "electric_total_energy_j": float(
                source["electric_total_energy_j"]
            ),
        })

    if not conversion_factors:
        raise ValueError("NO_NONZERO_MULTIPOLE")

    conversion = float(np.median(conversion_factors))

    if (
        conversion <= 0
        or max(
            abs(value / conversion - 1)
            for value in conversion_factors
        ) > 1e-7
    ):
        raise ValueError(
            "INCONSISTENT_CANONICAL_ENERGY_CONVERSION"
        )

    if not math.isclose(
        sum(m["electric_total_energy_j"] for m in modes),
        energy["new_electric_minimum_global_energy_j"],
        rel_tol=1e-7,
    ):
        raise ValueError("R3B_ELECTRIC_ENERGY_MISMATCH")

    if not math.isclose(
        normalization * (
            energy["new_magnetic_half_energy_j"]
            + energy["new_electric_minimum_global_energy_j"]
        ),
        REF,
        rel_tol=1e-9,
    ):
        raise ValueError("R3B_CAPACITY_PARTITION_DRIFT")

    return locks, modes, normalization, conversion


def shell(modes, normalization, conversion, n):
    mu, weights = leggauss(n)

    phi = np.zeros(n)
    e_out = np.zeros(n)
    e_in = np.zeros(n)
    e_tan = np.zeros(n)

    for mode in modes:
        ell = mode["ell"]
        amplitude = mode["amplitude"]

        coefficients = np.zeros(ell + 1)
        coefficients[-1] = 1.0

        polynomial = legval(mu, coefficients)
        derivative = legval(
            mu, legder(coefficients)
        )

        phi -= amplitude * polynomial / math.sqrt(2)

        e_out -= (
            (ell + 1) * amplitude * polynomial
            / (math.sqrt(2) * R)
        )

        e_in += (
            ell * amplitude * polynomial
            / (math.sqrt(2) * R)
        )

        e_tan -= (
            amplitude * np.sqrt(1 - mu**2) * derivative
            / (math.sqrt(2) * R)
        )

    charge = e_out - e_in
    average_field = (e_out + e_in) / 2

    area_weights = 2 * math.pi * R**2 * weights

    shell_energy = float(
        0.5 * np.dot(area_weights, charge * phi)
        * conversion * normalization
    )

    radial_force = (
        charge * average_field * conversion * normalization
    )

    tangential_force = (
        charge * e_tan * conversion * normalization
    )

    stress_jump_normal = (
        -(e_out**2 - e_in**2)
        * 0.5 * conversion * normalization
    )

    stress_jump_tangent = (
        -charge * e_tan * conversion * normalization
    )

    net_charge = float(np.dot(area_weights, charge))
    absolute_charge = float(
        np.dot(area_weights, np.abs(charge))
    )

    force_error = float(max(
        np.max(np.abs(radial_force + stress_jump_normal)),
        np.max(np.abs(tangential_force + stress_jump_tangent)),
    ))

    force_scale = max(
        1.0,
        float(np.max(np.abs(radial_force))),
        float(np.max(np.abs(tangential_force))),
    )

    threshold = 1e-14 * np.max(np.abs(charge))

    return {
        "n_mu": n,
        "net_charge_proxy": net_charge,
        "absolute_charge_proxy": absolute_charge,
        "net_over_absolute_charge": (
            abs(net_charge) / absolute_charge
            if absolute_charge > 0 else 1.0
        ),
        "surface_charge_energy_J": shell_energy,
        "max_radial_traction_Pa_equivalent": float(
            np.max(np.abs(radial_force))
        ),
        "max_tangential_traction_Pa_equivalent": float(
            np.max(np.abs(tangential_force))
        ),
        "radial_traction_rms_Pa_equivalent": float(
            np.sqrt(np.dot(weights, radial_force**2) / 2)
        ),
        "tangential_traction_rms_Pa_equivalent": float(
            np.sqrt(np.dot(weights, tangential_force**2) / 2)
        ),
        "stress_traction_scaled_error": (
            force_error / force_scale
        ),
        "positive_charge_area_fraction": float(
            np.dot(weights, charge > threshold) / 2
        ),
        "negative_charge_area_fraction": float(
            np.dot(weights, charge < -threshold) / 2
        ),
    }


def evaluate(modes, normalization, conversion):
    orders = (32, 48, 64, 96, 128, 192, 256, 384)
    cutoffs = list(range(1, len(modes) + 1))

    rows = []

    for cutoff in cutoffs:
        selected = modes[:cutoff]
        expected_energy = normalization * sum(
            m["electric_total_energy_j"]
            for m in selected
        )

        for order in orders:
            item = shell(
                selected, normalization, conversion, order
            )

            relative_error = abs(
                item["surface_charge_energy_J"] - expected_energy
            ) / max(expected_energy, 1e-30)

            item.update({
                "l_max": cutoff,
                "expected_energy_J": expected_energy,
                "energy_relative_error": relative_error,
            })

            if (
                relative_error > 5e-8
                or item["net_over_absolute_charge"] > 1e-9
                or item["stress_traction_scaled_error"] > 1e-11
            ):
                raise ValueError(
                    "SHELL_GAUSS_TRACTION_CHECK_FAILED"
                )

            rows.append(item)

    primary = rows[-1]

    historical = {
        "original_preloaded_capacity_J": REF,
        "strong_loaded_field_energy_J":
            1.5211390382733165,
        "strong_loaded_minimum_acceleration_m_s2":
            -129.67185782242464,
        "strong_loaded_peak_beta_1keV":
            18987.283771593688,
        "status":
            "HISTORICAL_NEGATIVE_CONTROL_NOT_REEXECUTED",
    }

    controls = {
        "zero_charge_cannot_produce_nonzero_mirror":
            primary["surface_charge_energy_J"] > 0
            and primary["absolute_charge_proxy"] > 0,
        "single_sign_charge_cannot_generate_bipolar_sheet":
            primary["positive_charge_area_fraction"] > 0
            and primary["negative_charge_area_fraction"] > 0
            and primary["net_over_absolute_charge"] < 1e-9,
        "zero_support_force_inconsistent":
            max(
                primary["max_radial_traction_Pa_equivalent"],
                primary["max_tangential_traction_Pa_equivalent"],
            ) > 0,
        "reverse_charge_changes_work_sign":
            -primary["surface_charge_energy_J"] < 0,
        "historical_loaded_inward_sign_preserved":
            historical[
                "strong_loaded_minimum_acceleration_m_s2"
            ] < 0,
    }

    if not all(controls.values()):
        raise ValueError("NEGATIVE_CONTROL_FAILED")

    # Necessary von Laue trace bound, only for the declared
    # standard Maxwell + static isolated DEC-remainder assumptions.
    # It is not a full R3B portal energy calculation.
    conditional_support = REF / 3

    result = {
        "program": "G01I_R3B_SOURCE_SUPPORT_AUDIT",
        "status":
            "PASS_NECESSARY_SHELL_OBLIGATIONS_NO_PHYSICAL_SOURCE",
        "protected_prescribed_R3B_capacity_J": REF,
        "multipole_count": len(modes),
        "multipole_cutoffs": cutoffs,
        "quadrature_orders": list(orders),
        "scanned_cases": len(rows),
        "electric_mirror_shell_energy_J":
            primary["expected_energy_J"],
        "electric_mirror_surface_charge_energy_J":
            primary["surface_charge_energy_J"],
        "primary_shell": primary,
        "negative_controls": controls,
        "historical_loaded_failure": historical,
        "conditional_DEC_remainder_energy_min_J":
            conditional_support,
        "conditional_field_plus_remainder_min_J":
            REF + conditional_support,
        "conditional_energy_assumptions":
            "STANDARD_MAXWELL_FIELD_STRESS;STATIC_ISOLATED_"
            "CONSERVED_COMPLETION;DEC_REMAINDER;NO_ADDITIONAL_"
            "PORTAL_HILBERT_STRESS",
        "source_requirements": {
            "electrostatic_shell_net_charge": "ZERO",
            "local_charge_signs":
                "BOTH_POSITIVE_AND_NEGATIVE_REQUIRED",
            "microscopic_charged_species":
                "NOT_CONSTRUCTED",
            "mechanical_support":
                "TRACTION_COMPUTED_NOT_SOURCED",
            "magnetic_current_source":
                "NOT_COMPLETED_HERE",
        },
        "gates": {
            "G00_ORIGINAL_R3B_PARENT": "PASS",
            "G01_COMPLETE_COVARIANT_ACTION": "MISSING",
            "G02_EXACT_VARIATIONS": "MISSING",
            "G03_MAXWELL_SHELL_IDENTITIES":
                "PASS_SCOPED",
            "G04_FULL_DYNAMICAL_STABILITY":
                "UNDETERMINED",
            "G05_SINGLE_SIGN_CHARGE_SHELL":
                "RULED_OUT_FOR_ORIGINAL_MIRROR",
            "G05_BIPOLAR_SOURCE_REALIZATION":
                "UNDETERMINED",
            "G06_LOADED_RESPONSE":
                "HISTORICAL_INWARD_FAILURE",
            "G07_EINSTEIN_METRIC":
                "NOT_DERIVED",
            "G08_COMPLETE_SI_ENERGY":
                "NOT_CERTIFIED",
            "G09_EXTERIOR_CONVERGENCE":
                "NOT_CLOSED",
            "G10_EARTH_CRAFT_REACTION":
                "NOT_DERIVED",
            "G11_EMPIRICAL_QUANTUM_UV":
                "NOT_DERIVED",
        },
        "physical_survivors": 0,
        "Einstein_gravity": "NOT_DERIVED",
        "whole_craft_lift": "NOT_DERIVED",
        "complete_operating_energy": "NOT_CERTIFIED",
        "006D_replaced": False,
        "next":
            "SPECIFY_NEW_COVARIANT_SOURCE_SUPPORT_ACTION_"
            "FOR_BIPOLAR_SHELL_AND_LOADED_SUSCEPTIBILITY",
    }

    return result, rows


def selftest():
    dipole = [{
        "ell": 1,
        "amplitude": 1.0,
    }]

    for order in (32, 64, 128):
        value = shell(dipole, 1.0, 1.0, order)

        assert abs(
            value["surface_charge_energy_J"]
            - math.pi * R
        ) < 1e-12

        assert value["net_over_absolute_charge"] < 1e-12
        assert value["stress_traction_scaled_error"] < 1e-12

    print("G01I_ANALYTIC_DIPOLE_SELFTEST=PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=("run", "selftest")
    )
    args = parser.parse_args()

    if args.command == "selftest":
        selftest()
        return 0

    import g01i_independent_v1 as independent

    parents, modes, normalization, conversion = parent()

    science, scan = evaluate(
        modes, normalization, conversion
    )

    independent.review(
        science, scan, modes, normalization, conversion
    )

    BASE.mkdir(parents=True, exist_ok=True)

    run_id = (
        datetime.now(timezone.utc).strftime(
            "g01i_%Y%m%dT%H%M%SZ_"
        ) + secrets.token_hex(4)
    )

    folder = BASE / run_id
    folder.mkdir(mode=0o700)

    source_names = (
        "g01i_r3b_source_v1.py",
        "g01i_independent_v1.py",
    )

    manifest = {
        "schema": "gravity2.g01i.v1",
        "run_id": run_id,
        "parent_sha256": parents,
        "source_sha256": {
            name: digest(ROOT / "scripts" / name)
            for name in source_names
        },
        "runtime": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
        },
    }

    sealed(folder / "manifest.json", encode(manifest))
    sealed(folder / "science.json", encode(science))
    sealed(folder / "mode_scan.json", encode(scan))

    if independent.verify(folder):
        return 3

    filenames = (
        "manifest.json",
        "science.json",
        "mode_scan.json",
        "verification.json",
    )

    ledger = "".join(
        digest(folder / name) + "  " + name + "\n"
        for name in filenames
    )

    sealed(
        folder / "SHA256SUMS.txt",
        ledger.encode()
    )

    archive = folder / (run_id + "_UPLOAD.tar.gz")

    with tarfile.open(archive, "x:gz") as bundle:
        for name in (*filenames, "SHA256SUMS.txt"):
            bundle.add(
                folder / name,
                arcname=run_id + "/" + name,
            )

    print("G01I_RUN=" + run_id)
    print("R3B_CAPACITY_J=" + str(REF))
    print("SCANNED_CASES=" + str(len(scan)))
    print(
        "CONDITIONAL_SUPPORT_MIN_J="
        + str(science["conditional_DEC_remainder_energy_min_J"])
    )
    print("HISTORICAL_LOADED_RESPONSE=INWARD_UNRESOLVED")
    print("PHYSICAL_SOURCE=NOT_DERIVED")
    print("UPLOAD_ARCHIVE=" + str(archive))
    print("UPLOAD_ARCHIVE_SHA256=" + digest(archive))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("G01I_HOLD=" + repr(exc), file=sys.stderr)
        raise SystemExit(3)
