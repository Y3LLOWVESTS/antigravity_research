from antigravity_research.agminer.learning import (
    BAND_ARCHIVE,
    BAND_MECHANISM,
    BAND_NEAR,
    BAND_TARGET,
    STRICT_TARGET_J,
    assess_energy,
    classify_energy,
)


def test_strict_target_boundary():
    assert classify_energy(9_999_999.0) == BAND_TARGET
    assert classify_energy(10_000_000.0) == BAND_NEAR


def test_near_miss_boundary():
    assert classify_energy(99_999_999.0) == BAND_NEAR
    assert classify_energy(100_000_000.0) == BAND_MECHANISM


def test_mechanism_boundary():
    assert classify_energy(1_000_000_000.0) == BAND_MECHANISM
    assert classify_energy(1_000_000_001.0) == BAND_ARCHIVE


def test_exact_10mj_is_not_certification_eligible():
    a = assess_energy(STRICT_TARGET_J)
    assert a.strict_energy_success is False
    assert a.certification_energy_eligible is False


def test_near_miss_priority():
    a = assess_energy(53_240_466.8716)
    assert a.band == BAND_NEAR
    assert a.learning_priority == "HIGH_LEARNING_PRIORITY"
    assert a.certification_energy_eligible is False


def test_proof_backed_floor_can_close_declared_branch():
    a = assess_energy(
        53_240_466.8716,
        proof_backed_floor_j=53_240_466.8716,
    )
    assert a.same_declared_branch_can_reach_target is False


def test_proof_backed_reducible_case():
    a = assess_energy(
        60_000_000.0,
        proof_backed_floor_j=8_000_000.0,
    )
    assert a.same_declared_branch_can_reach_target is True
    assert a.removable_energy_above_floor_j == 52_000_000.0


def test_negative_energy_rejected():
    try:
        classify_energy(-1.0)
    except ValueError:
        return
    raise AssertionError("negative energy must fail")
