"""Scientific regressions for 032V20 AGMINER family rerank."""

from antigravity_research.agminer.frontier_rerank import (
    closed_recipes,
    failure_memory_rules,
    family_recipe,
    persist_failure_memory,
    persist_frontier_metadata,
    ranked_active_recipes,
)
from antigravity_research.agminer.storage import (
    Storage,
)


def test_active_frontier_top_is_time_gradient_disformal():
    rows = ranked_active_recipes()

    assert (
        rows[
            0
        ].family_id
        ==
        "SHIFT_SYMMETRIC_TIME_GRADIENT_DISFORMAL_METRIC"
    )

    assert (
        rows[
            0
        ].tier
        ==
        "A"
    )


def test_second_active_family_is_propagating_nonmetricity():
    rows = ranked_active_recipes()

    assert (
        rows[
            1
        ].family_id
        ==
        "PROPAGATING_NONMETRICITY_HEALTHY_SINGLE_MODE"
    )

    assert (
        rows[
            1
        ].tier
        ==
        "A"
    )


def test_current_hidden_axial_implementation_is_closed():
    row = family_recipe(
        "CURRENT_HIDDEN_AXIAL_PURE_J0_KINETIC_CONFORMAL"
    )

    assert (
        row.closed
        is True
    )

    assert (
        row.status
        ==
        "CLOSED_R6"
    )


def test_current_closure_does_not_close_all_kinetic_conformal():
    row = family_recipe(
        "SHIFT_SYMMETRIC_TIME_GRADIENT_DISFORMAL_METRIC"
    )

    assert (
        row.closed
        is False
    )

    assert (
        "DISTINCT_FROM_CLOSED_STATIC_PURE_J0"
        in row.reason
    )


def test_goldstone_pure_j0_is_not_silently_repromoted():
    row = family_recipe(
        "SHIFT_PROTECTED_GOLDSTONE_KINETIC_METRIC_WITH_R5_EVASION"
    )

    assert (
        row.tier
        ==
        "B"
    )

    assert (
        "PURE_J0_LIMIT_BLOCKED_BY_R5_R6"
        in row.inherited_blockers
    )


def test_field_value_scalar_requires_new_protection():
    row = family_recipe(
        "PROTECTED_FIELD_VALUE_CONFORMAL_SCALAR_METRIC"
    )

    assert (
        "031F0"
        in row.inherited_blockers
    )

    assert (
        row.status
        ==
        "OPEN_ONLY_WITH_GENUINELY_NEW_PROTECTION"
    )


def test_pform_preserves_032r_tested_domain_closure():
    row = family_recipe(
        "MATTER_TRIGGERED_PFORM_BROADER_DOMAIN"
    )

    assert (
        "032R"
        in row.inherited_blockers
    )

    assert (
        row.closed
        is False
    )


def test_broad_scalar_tower_is_demoted_not_globally_closed():
    row = family_recipe(
        "BROAD_SPECTRAL_LINEAR_SCALAR_TOWER"
    )

    assert (
        row.closed
        is False
    )

    assert (
        row.tier
        ==
        "C"
    )


def test_failure_memory_policy_scopes_are_separate():
    rules = failure_memory_rules()

    current_operator = next(
        row
        for row in rules
        if (
            row[
                "family"
            ]
            ==
            "032_KINETIC_CONFORMAL_PURE_J0_STATIC_COEFFICIENT"
        )
    )

    current_implementation = next(
        row
        for row in rules
        if (
            row[
                "family"
            ]
            ==
            "032_HIDDEN_AXIAL_KINETIC_CONFORMAL_IMPLEMENTATION"
        )
    )

    assert (
        current_operator[
            "rule"
        ][
            "policy_specific"
        ]
        is False
    )

    assert (
        current_implementation[
            "rule"
        ][
            "policy_specific"
        ]
        is True
    )


def test_failure_memory_does_not_globally_close_kinetic_conformal():
    rules = failure_memory_rules()

    implementation = next(
        row
        for row in rules
        if (
            row[
                "family"
            ]
            ==
            "032_HIDDEN_AXIAL_KINETIC_CONFORMAL_IMPLEMENTATION"
        )
    )

    assert (
        implementation[
            "rule"
        ][
            "all_possible_kinetic_conformal_theories_closed"
        ]
        is False
    )


def test_failure_memory_persistence_is_idempotent(tmp_path):
    database = (
        tmp_path
        / "agminer_test.sqlite3"
    )

    storage = Storage(
        database
    )

    try:
        first = (
            persist_failure_memory(
                storage
            )
        )

        second = (
            persist_failure_memory(
                storage
            )
        )

        count = int(
            storage.connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM region_rules
                """
            ).fetchone()[
                "count"
            ]
        )

        assert (
            first
            ==
            len(
                failure_memory_rules()
            )
        )

        assert (
            second
            ==
            0
        )

        assert (
            count
            ==
            len(
                failure_memory_rules()
            )
        )

    finally:
        storage.close()


def test_rerank_memory_does_not_create_candidate_rows(tmp_path):
    database = (
        tmp_path
        / "agminer_test.sqlite3"
    )

    storage = Storage(
        database
    )

    try:
        persist_failure_memory(
            storage
        )

        model_count = int(
            storage.connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM models
                """
            ).fetchone()[
                "count"
            ]
        )

        rejection_count = int(
            storage.connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM rejections
                """
            ).fetchone()[
                "count"
            ]
        )

        mechanism_count = int(
            storage.connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM mechanism_metrics
                """
            ).fetchone()[
                "count"
            ]
        )

        assert (
            model_count
            ==
            0
        )

        assert (
            rejection_count
            ==
            0
        )

        assert (
            mechanism_count
            ==
            0
        )

    finally:
        storage.close()


def test_frontier_metadata_preserves_miner_and_no_model_claim(tmp_path):
    database = (
        tmp_path
        / "agminer_test.sqlite3"
    )

    storage = Storage(
        database
    )

    try:
        persist_frontier_metadata(
            storage
        )

        assert (
            storage.get_metadata(
                "agminer_itself_preserved"
            )
            ==
            "1"
        )

        assert (
            storage.get_metadata(
                "all_kinetic_conformal_theories_closed"
            )
            ==
            "0"
        )

        assert (
            storage.get_metadata(
                "physical_antigravity_model_found"
            )
            ==
            "0"
        )

        assert (
            storage.get_metadata(
                "certified_sub10mj_model_found"
            )
            ==
            "0"
        )

    finally:
        storage.close()
