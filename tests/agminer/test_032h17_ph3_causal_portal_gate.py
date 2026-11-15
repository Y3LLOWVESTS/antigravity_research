"""PH3 exact two-sector characteristic and negative-control regression."""

import math
import pytest

from antigravity_research.agminer.hook17_ph3_causal_portal_gate import (
    Background,
    characteristic,
    portal_derivatives,
    symbolic_checks,
    integrate_mode,
    provenance,
    run,
)


def test_symbolic_two_field_dispersion_and_hamiltonian():
    assert symbolic_checks()["scoped_exact_identity_checks"] == 13


@pytest.mark.parametrize(
    "law", ["linear", "even_negative", "even_positive"]
)
def test_portal_derivatives_against_independent_difference(law):
    p = .17
    coupling = .22
    h = 1e-5

    s, d, dd = portal_derivatives(law, coupling, p)
    spv = portal_derivatives(law, coupling, p+h)[0]
    smv = portal_derivatives(law, coupling, p-h)[0]

    assert (spv-smv)/(2*h) == pytest.approx(d, abs=3e-9)
    assert (spv+smv-2*s)/(h*h) == pytest.approx(
        dd, abs=3e-6
    )


@pytest.mark.parametrize(
    "electric,magnetic",
    [(.2, .7), (.2, 0), (0, .7), (-.2, .7)]
)
def test_positive_dust_linear_has_superluminal_extraordinary_mode(
    electric, magnetic
):
    rec = characteristic(
        Background("b", "linear", .6, .3, electric, magnetic)
    )

    assert rec["verdict"] == (
        "RED_SUPERLUMINAL_RESTRICTED_DUST"
    )
    assert rec["extraordinary_speed_over_physical_c"] > 1
    assert rec["electric_kinetic_coefficient"] > 0


@pytest.mark.parametrize(
    "rho,kappa", [(0, .3), (.6, 0)]
)
def test_no_material_curvature_gives_luminal(rho, kappa):
    rec = characteristic(
        Background("b", "linear", rho, kappa, .35, .7)
    )

    assert rec["material_curvature_chi"] == 0
    assert rec[
        "extraordinary_speed_over_physical_c"
    ] == pytest.approx(1)


def test_linear_portal_sign_flip_not_a_rescue():
    plus = characteristic(
        Background("plus", "linear", .6, .3, .3, .4)
    )
    minus = characteristic(
        Background("minus", "linear", .6, .3, -.3, .4)
    )

    assert plus["material_curvature_chi"] > 0
    assert minus["material_curvature_chi"] > 0
    assert plus["extraordinary_speed_over_physical_c"] > 1
    assert minus["extraordinary_speed_over_physical_c"] > 1


def test_even_negative_portal_can_be_sub_luminal_but_not_a_physical_model():
    rec = characteristic(
        Background("even", "even_negative", .35, .4, .35, .8)
    )

    assert rec["verdict"] == (
        "PASS_SCOPED_SUBLUMINAL_NOT_FULL_MODEL"
    )
    assert rec["sigma_prime"] != 0
    assert rec[
        "lawful_source_eom_and_support"
    ] == "NOT_DERIVED"


def test_even_portal_zero_p_has_no_linear_metric_response():
    rec = characteristic(
        Background("even", "even_negative", .35, .4, 0, .8)
    )

    assert rec["sigma_prime"] == 0
    assert rec["material_curvature_chi"] < 0


def test_linear_kinetic_failure_and_singular_metric_map_are_distinct():
    ghost = characteristic(
        Background("g", "linear", 2, 1, .15, 1)
    )
    singular = characteristic(
        Background("s", "linear", .01, 1, .5, .5)
    )

    assert ghost["verdict"] == (
        "RED_KINETIC_DEGENERATE_OR_NEGATIVE"
    )
    assert singular["verdict"] == (
        "RED_NONINVERTIBLE_CONFORMAL_MAP"
    )
    assert singular["electric_kinetic_coefficient"] > 0


def test_gradient_failure_separate_from_kinetic_failure():
    rec = characteristic(
        Background("grad", "even_negative", 1, 1, 2, .1)
    )

    assert rec["verdict"] == (
        "RED_GRADIENT_DEGENERATE_OR_NEGATIVE"
    )
    assert rec["electric_kinetic_coefficient"] > 0


def test_exact_critical_kinetic():
    rec = characteristic(
        Background("crit", "linear", 1, 1, 0, 1)
    )

    assert rec["electric_kinetic_coefficient"] == 0
    assert rec["verdict"] == (
        "RED_KINETIC_DEGENERATE_OR_NEGATIVE"
    )


@pytest.mark.parametrize(
    "case",
    [
        Background("lin", "linear", .7, .45, .35, .8),
        Background("vac", "linear", 0, .45, .35, .8),
        Background("even", "even_negative", .35, .4, .35, .8),
    ],
)
def test_numeric_generator_recovers_both_exact_characteristic_roots(case):
    result = integrate_mode(case, duration=2.5)

    assert result["numeric_speeds_over_c"] == pytest.approx(
        result["independent_analytic_speeds_over_c"],
        rel=1e-10,
    )
    assert result[
        "max_quadratic_energy_drift_shape_units"
    ] < 2e-9


def test_no_evolution_of_unhealthy_background():
    with pytest.raises(ValueError):
        integrate_mode(
            Background("ghost", "linear", 2, 1, .25, 1)
        )


@pytest.mark.parametrize(
    "case",
    [
        Background("neg", "linear", -1, .1, .3, .2),
        Background("bad", "linear", 1, -1, .3, .2),
        Background("inf", "linear", 1, .1, math.inf, .2),
        Background("nan", "linear", 1, .1, .3, math.nan),
        Background("overflow", "linear", 1, 100, 10, 10),
        Background("underflow", "even_negative", 1, 100, 10, 10),
    ],
)
def test_fail_closed_parameter_inputs(case):
    with pytest.raises(ValueError):
        characteristic(case)


def test_unknown_law_rejected():
    with pytest.raises(ValueError):
        portal_derivatives("unphysical", .2, .1)


def test_missing_archive_prevents_promotion(tmp_path):
    record = run(tmp_path)

    assert record["gates"][
        "P0_PRIOR_SOURCE_RESULTS"
    ] == "UNRESOLVED"
    assert record["gates"][
        "WHOLE_CRAFT_LIFT"
    ] == "NOT_ESTABLISHED"
    assert record["gates"][
        "B11_M6_FULL_CAUSAL_LOADED_IMPULSE"
    ] == "NOT_RUN"
    assert record["verdict"].startswith("YELLOW_")

    assert all(
        v["status"] == "MISSING"
        for v in provenance(tmp_path).values()
    )


def test_archival_hash_mismatch_never_passes(tmp_path):
    path = (
        tmp_path
        / "src/antigravity_research/agminer/"
        "hook17_ph2_source_causal_audit.py"
    )
    path.parent.mkdir(parents=True)
    path.write_text("different bytes")

    assert provenance(tmp_path)[
        "ph2_module"
    ]["status"] == "HASH_MISMATCH"
