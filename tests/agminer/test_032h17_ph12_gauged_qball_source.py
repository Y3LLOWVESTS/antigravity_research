"""PH12 independent trap-free scalar-Maxwell BVP tests and negative gates."""
from dataclasses import replace
import math

import numpy as np
import pytest

from antigravity_research.agminer import (
    hook17_ph12_gauged_qball_source as p
)


@pytest.fixture(scope="module")
def data(tmp_path_factory):
    return p.run(tmp_path_factory.mktemp("ph12_no_archive"))


@pytest.fixture(scope="module")
def central(data):
    return data["primary_gauged_equilibrium"]


def test_action_variations_derived_not_prescribed(data):
    a=data["exact_action_variations"]
    assert a["canonical_gauged_scalar_current"]=="PASS_EXACT"
    assert a["charged_scalar_Euler_Lagrange_equation"]=="PASS_EXACT"
    assert a["electrostatic_Gauss_action_derivative"]=="PASS_EXACT"
    assert a["gauge_phase_Ward_identity"]=="PASS_EXACT_OFF_SHELL"
    assert a["stationary_gauge_covariance"]=="PASS_EXACT"


def test_canonical_kinetic_principal_blocks(data):
    assert (
        data["exact_action_variations"][
            "canonical_kinetic_principal_blocks"
        ]=="PASS_BEFORE_GAUSS_CONSTRAINT"
    )
    assert data["gates"]["P1_RADIAL_DYNAMIC_STABILITY"]=="NOT_CERTIFIED"


def test_phi6_potential_positive_all_positive_amplitudes():
    s=np.geomspace(1e-12,1e4,2000)
    U=s-2*s*s+2*s*s*s
    assert np.all(U>=.5*s-1e-10)


def test_positive_potential_requires_input_gate():
    with pytest.raises(ValueError):
        p.solve(replace(p.Spec(),quartic=4.,sextic=.5))


def test_radial_mixed_portal_symmetry_control(data):
    v=data["exact_action_variations"]
    assert v["radial_mixed_portal_Y_variation"].startswith(
        "PASS_ONLY_SPHERICAL"
    )
    assert (
        v["nonradial_mixed_portal_Y_variation"]
        =="UNPROTECTED_BY_SYMMETRY"
    )
    assert data["gates"]["P2_FULL_UNIVERSAL_METRIC_CONSTITUTIVE"]=="NOT_SOLVED"


def test_joint_BVP_solved_nontrivial(central):
    assert central["BVP_status"]=="SOLVED"
    assert central["BVP_max_collocation_rms"]<1.1e-6
    assert central["positive_radial_mode"]
    assert 0<central["omega"]<1
    assert central["center_f"]==pytest.approx(.7)


def test_tail_localizes_without_trap(central):
    assert 0<central["tail_f_relative"]<1e-6
    assert central["no_external_square_well"]
    assert central["one_electric_U1_sector_only"]


def test_charge_from_same_current_matches_gauss(central):
    assert central["gauge_charge_integrated"]>0
    assert central["gauss_flux_at_boundary"]==pytest.approx(
        central["gauge_charge_integrated"],rel=3e-7
    )
    assert central["relative_gauss_flux_error"]<3e-7


def test_coulomb_exterior_energy_independent(central):
    Q=central["gauge_charge_integrated"]
    R=central["spec"]["radius"]
    tail=Q*Q/(8*math.pi*R)
    assert (
        central["canonical_energy"]["electric_Coulomb_outside"]
        ==pytest.approx(tail)
    )
    assert tail>0


def test_source_energy_ledger_complete_for_sector(central):
    e=central["canonical_energy"]
    terms=[
        "matter_time",
        "matter_gradient",
        "positive_scalar_potential",
        "electric_inside",
        "electric_Coulomb_outside",
    ]
    assert e[
        "scalar_plus_electromagnetic_total_including_Coulomb_tail"
    ]==pytest.approx(sum(e[k] for k in terms))
    assert all(e[k]>0 for k in terms)


def test_energy_free_quantum_criterion_is_necessary_only(central):
    assert (
        0<central["canonical_energy"]["energy_per_Noether_number"]
        <central["spec"]["scalar_mass"]
    )
    assert central["full_radial_spectral_stability"]=="NOT_CERTIFIED"


def test_local_radial_stress_conservation(central):
    assert central["exact_radial_stress_balance_max_residual"]<1e-4


def test_global_stress_virial_with_coulomb_tail(central):
    assert central["relative_integrated_stress_defect"]<5e-6
    assert central["integrated_spatial_trace_inside"]<0
    assert abs(
        central["integrated_spatial_trace_plus_Coulomb_tail"]
    )<1e-4


def test_radial_virial_surface_identity(central):
    assert central["virial_boundary_relative_error"]<5e-6
    assert central["virial_boundary_surface_term"]<0


def test_domain_convergence_E_Q(data,central):
    q=data["larger_domain_control"]
    assert q["radius"]==48
    assert abs(
        q["E_over_Q"]
        -central["canonical_energy"]["energy_per_Noether_number"]
    )<1e-5
    assert q["tail_relative"]<central["tail_f_relative"]


def test_independent_three_mesh_high_precision_convergence(data):
    cases=data["high_precision_mesh_control"]
    assert set(cases)=={"n220","n440","n880"}
    assert (
        max(x["omega"] for x in cases.values())
        -min(x["omega"] for x in cases.values())
    )<5e-9
    assert (
        max(x["E_over_Q"] for x in cases.values())
        -min(x["E_over_Q"] for x in cases.values())
    )<1e-8
    assert max(x["virial_rel"] for x in cases.values())<1e-8


def test_positive_charge_conjugate_exact(data,central):
    x=data["charge_conjugation"]
    assert x["negative_gauge_charge"]==pytest.approx(
        -central["gauge_charge_integrated"],rel=1e-10
    )
    assert x["negative_A0_at_center"]==pytest.approx(
        -central["A0_at_center"],abs=1e-10
    )
    assert x["same_matter_energy_isolated"]==pytest.approx(
        central["canonical_energy"][
            "scalar_plus_electromagnetic_total_including_Coulomb_tail"
        ],rel=1e-10
    )


def test_two_body_neutrality_is_not_equilibrium(data):
    a=data["charge_conjugation"]
    assert a["coupled_two_lump_equilibrium"]=="NOT_SOLVED"
    assert a[
        "leading_order_Coulomb_pair_at_separation_50"
    ]["attractive_radial_force"]<0
    assert a[
        "leading_order_Coulomb_pair_at_separation_50"
    ]["exact_composite_self_consistency"]=="NOT_SOLVED"


def test_global_U1_control(data):
    v=data["global_U1_no_gauge_control"]
    assert v["number"]>0 and v["energy"]>0
    assert (
        data["primary_gauged_equilibrium"]["canonical_energy"][
            "electric_inside"
        ]>0
    )


def test_low_amplitude_negative_control(data):
    q=data["unbound_branch_negative_control"]
    assert q["E_over_Q"]>1
    assert (
        q["classification"]
        =="POSITIVE_ENERGY_BUT_NOT_FREE_QUANTUM_BOUND"
    )


def test_gauge_repulsion_removes_free_quantum_binding(data):
    t=data["stronger_gauge_negative_control"]
    assert t["gauge_coupling"]==.2
    assert t["E_over_Q"]>1
    assert (
        t["classification"]
        =="ON_SHELL_BUT_FREE_QUANTUM_ENERGETICALLY_UNBOUND"
    )


def test_branch_slope_not_stability_proof(data):
    s=data["local_branch_stability_slope_control"]
    assert s["dQ_domega_finite_difference"]<0
    assert s["not_a_proof_of_full_spectral_stability"]


def test_no_Y_or_mixed_invariant_derived(data):
    assert data["gates"]["P2_SPINNING_MAGNETIC_Y_SOURCE"]=="NOT_SOLVED"
    assert data["gates"]["P3_1G_AT_1M_NEUTRAL_MATTER"]=="NOT_CERTIFIED"


def test_no_GR_lift_or_energy_promotion(data):
    a=data["gates"]
    assert a["P3_EARTH_DOWN_CRAFT_UP"]=="NOT_DERIVED"
    assert a["STRICT_COMPLETE_LT10MJ"]=="NOT_CERTIFIED"
    assert a["006D_REPLACED"]=="NO"
    assert a["P1_PHI6_UV_COMPLETION"]=="NOT_DERIVED"


def test_missing_history_is_unresolved(data):
    assert data["gates"]["P0_PROVENANCE"]=="UNRESOLVED"


def test_corrupted_history_is_detected(tmp_path):
    f=tmp_path/p.ARCHIVES["ph11_source"][0]
    f.parent.mkdir(parents=True)
    f.write_text("wrong previous source")
    assert (
        p.archive_status(tmp_path)["ph11_source"]["status"]
        =="HASH_MISMATCH"
    )


@pytest.mark.parametrize("bad",[
    {"gauge_coupling":-1},
    {"center_amplitude":0},
    {"radius":10},
    {"grid_nodes":30},
    {"tolerance":-1},
    {"quartic":8},
    {"scalar_mass":0},
    {"sextic":0},
    {"radius":float("nan")},
])
def test_bad_spec_rejected(bad):
    with pytest.raises(ValueError):
        p.solve(replace(p.Spec(),**bad))


@pytest.mark.parametrize("sign",[0,2,-2])
def test_charge_conjugation_input_fails_closed(sign):
    with pytest.raises(ValueError):
        p.solve(p.Spec(),charge_sign=sign)
