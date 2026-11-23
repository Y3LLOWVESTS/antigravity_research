"""GRAVITY2 v4 immutable L0/L1 review-contract catalog.

Scope: Four existing gates. Checks come from independent reviewer
results. Contracts validate their identities, exact keys, typed true
values, and non-promotion evidence.

These controls do NOT certify physical gravitational lift.
"""
from __future__ import annotations

from collections.abc import Mapping

_SCALAR = (
    "campaign_science",
    "campaign_check",
    "R3B_JORDAN_OPPOSITE_CHARGE_CONTROL",
)

_F0 = (
    "delta_f0_provider",
    "delta_f0_review",
    "R3B_F0_INTERFACE_AUDIT",
)

_GRIDS = (9, 15, 23, 31)

_PINS = (
    "R3B_SOURCE",
    "R3C_LOADED_SOURCE",
    "DELTA1_02_OPERATOR",
    "R3B_CAPACITY",
    "DELTA1_02_SCIENCE",
    "DELTA1_02_REVIEW",
)

_COMMON_F0 = {
    "registered gate and level",
    "candidate is source audit",
    "no physical promotion",
}

_CONTRACTS = {
    "ACTION_COMPLETENESS": (
        _SCALAR,
        "L0",
        "BLOCKED_ACTION_INCOMPLETE",
        {
            "missing covariant action sectors",
            "must block incomplete action",
            "not a physical completion",
        },
    ),

    "CHARGE_BALANCE_CONTROL": (
        _SCALAR,
        "L1",
        "SCOPED_CONTROL_ONLY",
        {
            "independent two-charge Euler",
            "equal-amplitude residual proportional to a",
            "opposing charge gauge shift",
            "four parent grid controls",
            "tuning not a physical equilibrium",
        } | {
            f"{label} n={n}"
            for n in _GRIDS
            for label in (
                "charge integral",
                "opposite current",
                "control frequency",
                "zero mode",
                "local source still nontrivial",
            )
        },
    ),

    "F0_PARENT_STATE_AUDIT": (
        _F0,
        "L0",
        "UNDERDETERMINED",
        _COMMON_F0
        | {f"live parent {p}" for p in _PINS}
        | {
            "parent status honest",
            "no automatic inverse",
            "no invented controls",
            "no certified loaded state",
            "loaded function inventory",
            "R3B loaded failure preserved",
            "field capacity not device energy",
        },
    ),

    "F0_LOADED_RECIPROCITY": (
        _F0,
        "L1",
        "SCOPED_CONTROL_ONLY",
        _COMMON_F0 | {
            "second derivative with curvature",
            "trace derivative",
            "transverse trace identity",
            "independent lambda sample",
            "independent second variation",
            "independent finite difference",
            "coupling-off null",
            "trace-off null",
            "omitted curvature rejected",
            "no sourceable JVP promotion",
            "no energy or craft promotion",
            "R3B loaded sign preserved",
        },
    ),
}

CONTRACTS = {
    key: {
        "pair": pair,
        "level": level,
        "verdict": verdict,
        "checks": frozenset(checks),
    }
    for key, (pair, level, verdict, checks)
    in _CONTRACTS.items()
}


def authorize_registration(job: dict) -> None:
    """Reject foreign or incorrectly leveled gate providers."""
    if not isinstance(job, dict):
        raise ValueError("V4_TASK_TYPE")

    rule = CONTRACTS.get(job.get("gate"))

    if rule is None:
        raise ValueError("V4_UNREGISTERED_REVIEW_CONTRACT")

    actual = (
        job.get("module"),
        job.get("independent"),
        job.get("candidate"),
    )

    if (
        actual != rule["pair"]
        or job.get("level") != rule["level"]
    ):
        raise ValueError("V4_PROVIDER_OR_LEVEL_MISMATCH")


def enforce(job: dict, evidence: dict, checks: Mapping) -> dict:
    """Require exact review and preserve incomplete-physics verdicts."""
    authorize_registration(job)

    rule = CONTRACTS[job["gate"]]

    if (
        not isinstance(evidence, dict)
        or evidence.get("status") != rule["verdict"]
    ):
        raise ValueError("V4_VERDICT_MISMATCH")

    if (
        not isinstance(checks, Mapping)
        or set(checks) != rule["checks"]
    ):
        raise ValueError("V4_REVIEW_KEYSET_MISMATCH")

    if not all(
        type(v) is bool and v
        for v in checks.values()
    ):
        raise ValueError("V4_REVIEW_FALSE_OR_NONBOOLEAN")

    gate = job["gate"]

    if gate == "ACTION_COMPLETENESS":
        ok = (
            evidence.get("complete_covariant_action")
            == "NOT_DERIVED"
            and isinstance(
                evidence.get("missing_action_terms"), list
            )
            and bool(evidence["missing_action_terms"])
        )

    elif gate == "CHARGE_BALANCE_CONTROL":
        rows = evidence.get("rows")

        ok = (
            evidence.get("full_Einstein_support")
            == "NOT_DERIVED"
            and "NOT_AN_EOM" in str(
                evidence.get("zero_mode_tuning", "")
            )
            and isinstance(rows, list)
            and [
                r.get("grid") for r in rows
            ] == list(_GRIDS)
            and all(
                r.get("scalar_and_X_stationary")
                == "NOT_TESTED"
                for r in rows
            )
        )

    elif gate == "F0_PARENT_STATE_AUDIT":
        ok = (
            evidence.get("constraint_projected_JVP")
            == "NOT_DEFINED"
            and evidence.get("sourceable_control_map")
            == "NOT_DERIVED"
            and evidence.get(
                "on_shell_loaded_state_for_differentiation"
            ) == "NOT_CERTIFIED"
            and evidence.get("historical_failure_m_s2")
            == -129.67185782242464
            and evidence.get("R3B_field_only_J")
            == 1.5429162116460216
        )

    else:
        ok = (
            evidence.get("response_projection")
            == "NO_NEW_SOURCEABLE_OPERATOR_OR_JVP_TO_TEST"
            and evidence.get("complete_SI_energy")
            == "NOT_CERTIFIED"
            and evidence.get("Earth_and_craft")
            == "NOT_DERIVED"
            and evidence.get("R3B_loaded_failure_m_s2")
            == -129.67185782242464
        )

    if not ok:
        raise ValueError("V4_UNSUPPORTED_PHYSICAL_PROMOTION")

    return dict(checks)
