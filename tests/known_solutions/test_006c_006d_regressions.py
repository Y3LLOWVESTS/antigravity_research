"""Regression protection for Simulations 006C and 006D.

PURPOSE
-------
Protect the two final classical-GR verification milestones completed before
the project moves to the established-quantum-physics branch.

Simulation 006C independently reconstructed the Simulation 005B finite-disk
field using direct numerical Green-function integration rather than the 005B
analytic field implementation.

Simulation 006D constructed a finite-radius, finite-thickness, locally
conserved stress-energy configuration satisfying the classical pointwise
energy conditions within the static linearized-GR model.

SCIENTIFIC REGRESSIONS PROTECTED
--------------------------------
Simulation 006C:

- the 30-point independent Green-function field comparison;
- the repulsive zero z_zero / R;
- the independently reconstructed optimum R / h;
- the independently reconstructed 005B mass coefficient.

Simulation 006D:

- local control-volume conservation;
- NEC, WEC, and DEC;
- integrated static stress balance;
- monotonic finite-thickness convergence toward the 006B thin result;
- the finest tested finite-thickness coefficient;
- conservative claim boundaries.

METHOD
------
The simulations are executed as subprocesses using the current Python
interpreter.

Each simulation is run only once per pytest process. Its independently
reconstructed scientific output is then parsed and checked against the
established benchmark values and acceptance thresholds.

This deliberately avoids copying the scientific equations into the test file.
The tests therefore protect the actual executable simulations rather than a
second handwritten transcription.

INDEPENDENCE / CLAIM LIMIT
--------------------------
These are regression tests.

They do not constitute a new independent scientific derivation. Simulation
006C itself remains the independent numerical implementation relative to the
005B analytic field calculation.

Passing these tests does not establish:

- exact nonlinear general relativity;
- dynamical stability;
- a known material realization;
- experimental accessibility;
- a practical antigravity device.

RELATED FILES
-------------
simulations/006c_independent_finite_disk_field.py
simulations/006d_finite_thickness_conserved_source.py
src/antigravity_research/geometry/finite_tension_disk.py
src/antigravity_research/geometry/axisymmetric_thin_stress.py

CLAIM CLASSIFICATION
--------------------
REGRESSION_PROTECTION
"""

from __future__ import annotations

import functools
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
SIMULATIONS = ROOT / "simulations"


@functools.lru_cache(maxsize=None)
def _run_simulation(filename: str) -> str:
    """Run one scientific simulation and return its standard output.

    The repository ``src`` directory is added explicitly to ``PYTHONPATH`` so
    the test does not depend on editable-install state or the caller's shell
    configuration.
    """

    environment = os.environ.copy()

    existing_pythonpath = environment.get("PYTHONPATH")

    if existing_pythonpath:
        environment["PYTHONPATH"] = (
            f"{ROOT / 'src'}"
            f"{os.pathsep}"
            f"{existing_pythonpath}"
        )
    else:
        environment["PYTHONPATH"] = str(ROOT / "src")

    completed = subprocess.run(
        [
            sys.executable,
            str(SIMULATIONS / filename),
        ],
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
        timeout=180,
    )

    if completed.returncode != 0:
        raise AssertionError(
            "Scientific regression simulation failed.\n"
            f"FILE={filename}\n"
            f"RETURN_CODE={completed.returncode}\n"
            "--- STDOUT ---\n"
            f"{completed.stdout}\n"
            "--- STDERR ---\n"
            f"{completed.stderr}"
        )

    return completed.stdout


def _value(
    output: str,
    key: str,
) -> str:
    """Return the final KEY=value result emitted by a simulation."""

    matches = re.findall(
        rf"^{re.escape(key)}=(.+)$",
        output,
        flags=re.MULTILINE,
    )

    if not matches:
        raise AssertionError(
            f"Missing scientific result label: {key}"
        )

    return matches[-1].strip()


def _float_value(
    output: str,
    key: str,
) -> float:
    """Return a floating-point simulation result."""

    return float(
        _value(
            output,
            key,
        )
    )


def test_006c_independent_green_function_field_grid() -> None:
    """Protect the independent 30-point 006C field reconstruction."""

    output = _run_simulation(
        "006c_independent_finite_disk_field.py"
    )

    assert _value(
        output,
        "PRIMARY_FIELD_IMPLEMENTATION_REUSES_005B_ANALYTIC_FORMULA",
    ) == "NO"

    assert int(
        _value(
            output,
            "COMPARISON_POINT_COUNT",
        )
    ) == 30

    assert (
        _float_value(
            output,
            "MAX_ABSOLUTE_FIELD_ERROR",
        )
        < 1.0e-10
    )

    assert (
        _float_value(
            output,
            "MAX_RELATIVE_FIELD_ERROR",
        )
        < 1.0e-10
    )

    assert _value(
        output,
        "FIELD_GRID_MATCH",
    ) == "PASS"

    assert _value(
        output,
        "FIELD_GRID_VERIFIED",
    ) == "YES"


def test_006c_repulsive_zero_regression() -> None:
    """Protect the independently reconstructed 005B repulsive zero."""

    output = _run_simulation(
        "006c_independent_finite_disk_field.py"
    )

    zero = _float_value(
        output,
        "NUMERIC_Z_ZERO_OVER_R",
    )

    assert abs(
        zero
        - 0.393319893190334
    ) < 1.0e-12

    assert (
        _float_value(
            output,
            "ZERO_ABSOLUTE_ERROR",
        )
        < 1.0e-9
    )

    assert _value(
        output,
        "REPULSIVE_ZERO_MATCH",
    ) == "PASS"

    assert _value(
        output,
        "REPULSIVE_ZERO_VERIFIED",
    ) == "YES"


def test_006c_independent_optimum_regression() -> None:
    """Protect the independent 005B optimum geometry and coefficient."""

    output = _run_simulation(
        "006c_independent_finite_disk_field.py"
    )

    radius_over_height = _float_value(
        output,
        "OPTIMAL_R_OVER_H",
    )

    coefficient = _float_value(
        output,
        "NUMERIC_005B_COEFFICIENT",
    )

    assert abs(
        radius_over_height
        - 4.006149730747969
    ) < 1.0e-6

    assert abs(
        coefficient
        - 79.753148116012255
    ) < 1.0e-6

    assert _value(
        output,
        "005B_OPTIMUM_MATCH",
    ) == "PASS"

    assert _value(
        output,
        "005B_OPTIMUM_VERIFIED",
    ) == "YES"

    assert _value(
        output,
        "SIMULATION_006C",
    ) == "GREEN"

    assert _value(
        output,
        "CLAIM_CLASSIFICATION",
    ) == "INDEPENDENT_NUMERICAL_VERIFICATION"


def test_006d_local_conservation_and_energy_conditions() -> None:
    """Protect 006D conservation, stress balance, and energy conditions."""

    output = _run_simulation(
        "006d_finite_thickness_conserved_source.py"
    )

    assert (
        _float_value(
            output,
            "MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL",
        )
        < 1.0e-8
    )

    assert (
        _float_value(
            output,
            "MAX_DEC_VIOLATION",
        )
        <= 1.0e-12
    )

    assert (
        _float_value(
            output,
            "MIN_NEC_MARGIN",
        )
        >= -1.0e-12
    )

    assert (
        _float_value(
            output,
            "MAX_INTEGRATED_STRESS_TRACE",
        )
        < 1.0e-8
    )

    assert _value(
        output,
        "LOCAL_CONSERVATION",
    ) == "PASS"

    assert _value(
        output,
        "NEC",
    ) == "PASS"

    assert _value(
        output,
        "WEC",
    ) == "PASS"

    assert _value(
        output,
        "DEC",
    ) == "PASS"

    assert _value(
        output,
        "LAUE_STRESS_BALANCE",
    ) == "PASS"


def test_006d_finite_thickness_converges_to_thin_limit() -> None:
    """Protect the established finite-thickness convergence sequence."""

    output = _run_simulation(
        "006d_finite_thickness_conserved_source.py"
    )

    coefficient_matches = re.findall(
        r"^SCALE=([0-9.]+).*?C=([0-9.]+)",
        output,
        flags=re.MULTILINE,
    )

    assert len(coefficient_matches) == 7

    scales = [
        float(scale)
        for scale, _ in coefficient_matches
    ]

    coefficients = [
        float(coefficient)
        for _, coefficient in coefficient_matches
    ]

    assert scales == [
        0.40000,
        0.20000,
        0.10000,
        0.05000,
        0.02500,
        0.01250,
        0.00625,
    ]

    assert all(
        later < earlier
        for earlier, later in zip(
            coefficients[:-1],
            coefficients[1:],
        )
    )

    assert abs(
        coefficients[0]
        - 38.037638025730
    ) < 1.0e-9

    assert abs(
        coefficients[-1]
        - 23.591586299249
    ) < 1.0e-9

    assert abs(
        _float_value(
            output,
            "THIN_REFERENCE_C",
        )
        - 23.426710175391
    ) < 1.0e-12

    assert abs(
        _float_value(
            output,
            "FINEST_FINITE_C",
        )
        - 23.591586299249
    ) < 1.0e-9

    assert (
        _float_value(
            output,
            "FINEST_RELATIVE_ERROR",
        )
        < 0.01
    )

    assert _value(
        output,
        "MONOTONIC_APPROACH_TO_THIN",
    ) == "YES"

    assert _value(
        output,
        "THIN_LIMIT_RECOVERY",
    ) == "PASS"


def test_006d_summary_and_claim_boundaries() -> None:
    """Protect the 006D result classification without overclaiming it."""

    output = _run_simulation(
        "006d_finite_thickness_conserved_source.py"
    )

    assert _value(
        output,
        "FINITE_SPATIAL_SUPPORT",
    ) == "YES"

    assert _value(
        output,
        "FINITE_THICKNESS",
    ) == "YES"

    assert _value(
        output,
        "SINGULAR_OUTER_RING",
    ) == "NO"

    assert _value(
        output,
        "POINTWISE_NEC_WEC_DEC",
    ) == "YES"

    assert _value(
        output,
        "LOCAL_CONSERVATION_LINEARIZED_ORDER",
    ) == "YES"

    assert _value(
        output,
        "OUTWARD_GRAVITATIONAL_FIELD",
    ) == "YES"

    assert _value(
        output,
        "POSITIVE_FAR_FIELD_ACTIVE_MASS",
    ) == "YES"

    assert abs(
        _float_value(
            output,
            "C_FINITE_BEST_TESTED",
        )
        - 23.591586299249
    ) < 1.0e-9

    assert _value(
        output,
        "SIMULATION_006D",
    ) == "GREEN"

    assert _value(
        output,
        "CLAIM_CLASSIFICATION",
    ) == "CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT"

    # These negative assertions are scientifically important.  A future
    # documentation or implementation change must not silently promote the
    # linearized construction beyond what has actually been established.
    assert _value(
        output,
        "EXACT_NONLINEAR_GR_CONSERVATION",
    ) == "NOT_ESTABLISHED"

    assert _value(
        output,
        "DYNAMIC_STABILITY",
    ) == "NOT_ESTABLISHED"

    assert _value(
        output,
        "KNOWN_MATERIAL_REALIZATION",
    ) == "NO"

    assert _value(
        output,
        "PRACTICAL_ANTIGRAVITY_DEVICE",
    ) == "NO"
