from antigravity_research.agminer.learning_provenance import (
    PROVENANCE_CURRENT,
    PROVENANCE_SUPERSEDED,
    assess_family_provenance,
)


def test_032c_quantitative_energy_is_superseded():
    p = assess_family_provenance("032C_TWIN_PNGB_DBI_METRIC")
    assert p.status == PROVENANCE_SUPERSEDED
    assert p.usable_for_active_energy_ranking is False
    assert p.historical_lesson_preserved is True


def test_032e_quantitative_energy_is_superseded():
    p = assess_family_provenance("032E_COLLECTIVE_MULTISCALAR_TWIN_PNGB")
    assert p.status == PROVENANCE_SUPERSEDED
    assert p.usable_for_active_energy_ranking is False


def test_corrected_032h_not_marked_superseded():
    p = assess_family_provenance("032H_SOURCE_AWARE_COLLECTIVE_DBI")
    assert p.status == PROVENANCE_CURRENT
    assert p.usable_for_active_energy_ranking is True


def test_032n1_not_marked_superseded():
    p = assess_family_provenance("032N1_GHOST_CONDENSATE_ONE_SIDED_CONTINUUM_BOUND")
    assert p.status == PROVENANCE_CURRENT


def test_supersession_does_not_mean_history_deleted():
    p = assess_family_provenance("032C_TWIN_PNGB_DBI_METRIC")
    assert p.historical_lesson_preserved is True
