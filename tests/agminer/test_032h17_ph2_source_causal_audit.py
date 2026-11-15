"""PH2 source equilibrium, reciprocal kinetic and recoil controls."""
import numpy as np
import pytest

from antigravity_research.agminer.hook17_ph2_source_causal_audit import (
    WaveSpec,
    _envelope,
    _derivative,
    exact_algebra,
    source_shape_integrals,
    static_no_go,
    initial_state,
    causal_source_run,
    restricted_kinetic,
    provenance,
    energy_gate,
    execute,
)


def test_exact_restricted_dust_variations():
    result = exact_algebra()
    assert result["identities_passed"] >= 10
    assert result["invertibility_factor"] == "1-4*kappa*P"


@pytest.mark.parametrize(
    "mass",
    [0.0, 0.25, 1.0, 2.0],
)
def test_free_source_eom_positive_integral(mass):
    result = source_shape_integrals(mass=mass)

    assert result["free_static_no_go_integral"] > 0
    assert result["azimuthal_gradient"] > 0
    assert result["radial_gradient"] > 0
    assert result["axial_gradient"] > 0

    if mass > 0:
        assert result["rest_mass"] > 0


def test_winding_integral_recovers_ph1_angular_cost():
    assert source_shape_integrals()[
        "azimuthal_gradient"
    ] == pytest.approx(
        0.34543615403812755,
        abs=1e-11,
    )


@pytest.mark.parametrize(
    "order",
    [36, 60, 90],
)
def test_winding_quadrature_converges(order):
    result = source_shape_integrals(
        order=order,
        angular=128,
    )

    reference = source_shape_integrals(
        order=110,
        angular=160,
    )

    assert result[
        "free_static_no_go_integral"
    ] == pytest.approx(
        reference["free_static_no_go_integral"],
        abs=2e-7,
    )


def test_static_nogo_scope_is_explicit():
    result = static_no_go()

    assert result[
        "M5I_free_scalar_Aphi_zero"
    ] == "SCOPED_NO_GO"

    assert result["physical_source_energy_j"] is None

    assert "self interactions" in result[
        "reopening_conditions"
    ]


def test_negative_mass_input_rejected():
    with pytest.raises(ValueError):
        source_shape_integrals(mass=-1)

    with pytest.raises(ValueError):
        source_shape_integrals(order=2)


@pytest.mark.parametrize(
    "b2,expected",
    [
        (0, 1),
        (0.0625, 0.9375),
        (1, 0),
        (4, -3),
    ],
)
def test_restricted_kinetic_boundary(b2, expected):
    result = restricted_kinetic(
        1, 1, 0, b2
    )

    assert result["loaded_eigenvalue"] == pytest.approx(
        expected
    )

    assert result["positive_necessary"] == (
        expected > 0
    )

    assert result[
        "full_characteristic_health"
    ] == "NOT_TESTED"


def test_conformal_jacobian_zero_is_excluded():
    assert not restricted_kinetic(
        1, 1, 0.25, 0
    )["invertible_necessary"]

    assert restricted_kinetic(
        1, 1, 0, 0
    )["invertible_necessary"]


@pytest.mark.parametrize(
    "rho,b2",
    [
        (-1, 1),
        (1, -0.01),
        (float("nan"), 1),
    ],
)
def test_restricted_kinetic_bad_input_fails(rho, b2):
    with pytest.raises(ValueError):
        restricted_kinetic(
            rho, 1, 0, b2
        )


def test_source_envelope_finite_support():
    x = np.linspace(-1, 1, 2001)

    f, fx = _envelope(
        x, 0.1, 0.34
    )

    assert np.all(f >= 0)
    assert np.all(f[abs(x-0.1) > 0.34] == 0)
    assert np.all(fx[abs(x-0.1) > 0.34] == 0)

    assert np.trapezoid(f, x) == pytest.approx(
        1, abs=1e-8
    )


def test_source_envelope_translation_derivative():
    x = np.linspace(-1, 1, 501)
    h = 1e-5

    f, fx = _envelope(
        x, 0.07, 0.34
    )

    fp, _ = _envelope(
        x, 0.07+h, 0.34
    )

    fm, _ = _envelope(
        x, 0.07-h, 0.34
    )

    assert np.max(
        abs((fp-fm)/(2*h)+fx)
    ) < 1e-6


def test_field_source_off_is_exact_equilibrium():
    spec = WaveSpec(n=96)

    x = np.linspace(
        -spec.length/2,
        spec.length/2,
        spec.n,
        endpoint=False,
    )

    y = initial_state(
        spec, "source_off", x
    )

    derivative = _derivative(
        0, y, spec, x,
        spec.length/spec.n,
    )

    assert np.all(derivative == 0)


def test_source_current_from_eom_not_prescribed_waveform():
    spec = WaveSpec(n=96)

    x = np.linspace(
        -spec.length/2,
        spec.length/2,
        spec.n,
        endpoint=False,
    )

    y = initial_state(
        spec, "self_sourced", x
    )

    derivative = _derivative(
        0, y, spec, x,
        spec.length/spec.n,
    )

    assert not np.all(derivative == 0)
    assert not np.any(np.isnan(derivative))


@pytest.mark.parametrize(
    "case",
    [
        "source_off",
        "self_sourced",
        "incoming_recoil",
    ],
)
def test_reduced_action_energy_conservation(case):
    result = causal_source_run(
        WaveSpec(n=128, tmax=1.4),
        case,
    )

    assert result["max_energy_absolute_drift"] < 1e-8
    assert result["impulse_integral_residual"] < 1e-6

    assert result[
        "craft_upward_impulse"
    ] == "NOT_DERIVED"

    assert result[
        "radiation_flux_to_infinity"
    ] == "NOT_MODELED_PERIODIC_BOX"


def test_source_off_zero_energy_momentum_impulse():
    result = causal_source_run(
        WaveSpec(n=96, tmax=1.4),
        "source_off",
    )

    assert result["initial_energy"] == 0
    assert result["final_carrier_energy"] == 0
    assert result["max_total_momentum_drift"] == 0

    assert result[
        "source_center_signed_impulse"
    ] == [0, 0]


def test_source_energy_transferred_to_waves():
    result = causal_source_run(
        WaveSpec(n=128, tmax=2.1),
        "self_sourced",
    )

    assert result["initial_source_energy"] > 0
    assert result["final_carrier_energy"] > 0

    assert (
        result["final_source_energy"]
        < result["initial_source_energy"]
    )

    assert result["max_total_momentum_drift"] < 3e-5


def test_incoming_wave_recoil_field_momentum():
    result = causal_source_run(
        WaveSpec(n=256, tmax=2.1),
        "incoming_recoil",
    )

    assert result[
        "source_center_signed_impulse"
    ][0] > 0

    assert result["max_total_momentum_drift"] < 5e-6

    assert result[
        "source_center_momentum_change"
    ][0] > 0

    assert result["impulse_integral_residual"] < 1e-7


@pytest.mark.parametrize(
    "case",
    ["not_a_case", "propulsion"],
)
def test_invalid_wave_case_rejected(case):
    spec = WaveSpec()

    x = np.linspace(
        -4, 4, spec.n,
        endpoint=False,
    )

    with pytest.raises(ValueError):
        initial_state(spec, case, x)


@pytest.mark.parametrize(
    "bad",
    [
        WaveSpec(n=40),
        WaveSpec(n=99),
        WaveSpec(width=-1),
    ],
)
def test_wave_spec_bad_input_rejected(bad):
    with pytest.raises(ValueError):
        causal_source_run(bad)


def test_field_only_energy_not_device_certificate():
    result = energy_gate({
        "all_loaded_carrier_fields":
            1.5429162116460216
    })

    assert result["status"] == "NOT_CERTIFIED"

    assert (
        "physical_source_rest_internal"
        in result["missing_components"]
    )


@pytest.mark.parametrize(
    "value",
    [10_000_000, 10_000_001],
)
def test_strict_energy_threshold(value):
    result = energy_gate({
        "physical_source_rest_internal": value
    })

    assert result[
        "status"
    ] == "FAIL_KNOWN_ENERGY_GE10MJ"


def test_invalid_energy_fails_closed():
    with pytest.raises(ValueError):
        energy_gate({
            "physical_source_rest_internal": -1
        })

    with pytest.raises(ValueError):
        energy_gate({
            "physical_source_rest_internal":
                float("nan")
        })


def test_missing_archives_never_gain_promotion(tmp_path):
    archive = provenance(tmp_path)

    assert archive[
        "m5v_code"
    ]["status"] == "MISSING"

    assert not archive["ph1_result_present"]

    result = execute(tmp_path)

    assert result["gates"][
        "PH2_PROVENANCE"
    ] == "UNRESOLVED"

    assert result["gates"][
        "PH2_EARTH_DOWN_CRAFT_UP"
    ] == "NOT_DERIVED"

    assert result["gates"][
        "PH2_COMPLETE_LT10MJ"
    ] == "NOT_CERTIFIED"

    assert result["gates"][
        "PH2_B11_M6_FULL_LOADED_STATIC_REPRODUCTION"
    ] == "NOT_RUN"

    assert result["gates"][
        "PH2_ENGINE_OR_LIFT"
    ] == "NOT_ESTABLISHED"


def test_binary_hash_mismatch_fails_closed(tmp_path):
    path = (
        tmp_path
        / "src/antigravity_research/agminer/"
        "hook17_ph1_physicalization_preflight.py"
    )

    path.parent.mkdir(parents=True)

    path.write_text(
        "different source",
        encoding="utf-8",
    )

    assert provenance(tmp_path)[
        "ph1_code"
    ]["status"] == "MISMATCH"
